# ui/generator_dialog.py

"""
    Dialogue de génération de mot de passe.
    Supporte deux modes : mot de passe aléatoire et passphrase.
"""

# ----- IMPORTS ----- 
from __future__ import annotations
import secrets
import string

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QCheckBox, QPushButton, QRadioButton, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui  import QGuiApplication

from ui.theme import *
from services.strength import strength, score_to_label

DEFAULT_WORDS = [
    "lune","pierre","tigre","mer","forêt","orange","neon","pixel","delta","vortex",
    "brise","astro","kilo","sigma","quartz","cobra","opera","ninja","python","foudre"
]

class GeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Générateur de mot de passe")
        self.setMinimumWidth(380)
        self.setStyleSheet(f"""
            QDialog     {{ background-color: {BG_DEEP}; }}
            QLabel      {{ color: {TEXT_PRI}; }}
            QRadioButton{{ color: {TEXT_SEC}; }}
            QCheckBox   {{ color: {TEXT_SEC}; }}
            QSpinBox {{
                background: {BG_CARD}; color: {TEXT_PRI};
                border: 1px solid {BORDER_LT}; border-radius: 4px; padding: 2px 6px;
            }}
            QLineEdit {{
                background: {BG_CARD}; color: {TEXT_PRI};
                border: 1px solid {BORDER_LT}; border-radius: 4px; padding: 2px 8px;
            }}
            QPushButton {{
                background: {BG_HOVER}; color: {VIOLET_LT};
                border: 1px solid {BORDER_LT}; border-radius: 4px;
                padding: 4px 12px;
            }}
            QPushButton:hover {{ background: {BG_CARD}; }}
            QProgressBar {{
                background: {BG_CARD}; border: 1px solid {BORDER};
                border-radius: 4px; height: 8px; text-align: center;
            }}
            QProgressBar::chunk {{ background: {VIOLET}; border-radius: 4px; }}
        """)

        # ----- Widgets -----
        self.out = QLineEdit()
        self.out.setEchoMode(QLineEdit.Password)
        self.out.setFixedHeight(36)

        self.btn_show   = QCheckBox("Afficher")
        self.rb_pwd     = QRadioButton("Mot de passe")
        self.rb_pwd.setChecked(True)
        self.rb_phrase  = QRadioButton("Passphrase")

        self.spin_len   = QSpinBox()
        self.spin_len.setRange(8, 128)
        self.spin_len.setValue(20)

        self.cb_lower   = QCheckBox("a-z");     self.cb_lower.setChecked(True)
        self.cb_upper   = QCheckBox("A-Z");     self.cb_upper.setChecked(True)
        self.cb_digits  = QCheckBox("0-9");     self.cb_digits.setChecked(True)
        self.cb_symbols = QCheckBox("Symboles");self.cb_symbols.setChecked(True)
        self.cb_ambig   = QCheckBox("Éviter ambigus (l/1, O/0)")

        self.spin_words = QSpinBox()
        self.spin_words.setRange(3, 12)
        self.spin_words.setValue(5)

        self.sep = QLineEdit("-")
        self.sep.setMaxLength(3)
        self.sep.setFixedWidth(48)

        self.meter      = QProgressBar()
        self.meter.setRange(0, 4)
        self.meter.setFixedHeight(8)
        self.lbl_score  = QLabel("Score : –")
        self.lbl_score.setStyleSheet(f"color: {TEXT_SEC}; font-size: 12px;")

        self.btn_generate = QPushButton("Générer")
        self.btn_copy     = QPushButton("Copier")
        self.btn_ok       = QPushButton("Utiliser ce mot de passe")
        self.btn_ok.setDefault(True)
        self.btn_ok.setStyleSheet(f"""
            QPushButton {{
                background-color: {VIOLET}; color: {VIOLET_XLT};
                border: none; border-radius: 4px; padding: 6px 16px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: #6d28d9; }}
        """)

        # ----- Layout -----
        L = QVBoxLayout(self)
        L.setSpacing(10)
        L.setContentsMargins(20, 20, 20, 20)

        row_mode = QHBoxLayout()
        row_mode.addWidget(self.rb_pwd)
        row_mode.addWidget(self.rb_phrase)
        L.addLayout(row_mode)

        row_len = QHBoxLayout()
        row_len.addWidget(QLabel("Longueur :"))
        row_len.addWidget(self.spin_len)
        L.addLayout(row_len)

        L.addWidget(self.cb_lower)
        L.addWidget(self.cb_upper)
        L.addWidget(self.cb_digits)
        L.addWidget(self.cb_symbols)
        L.addWidget(self.cb_ambig)

        row_words = QHBoxLayout()
        row_words.addWidget(QLabel("Mots :"))
        row_words.addWidget(self.spin_words)
        L.addLayout(row_words)

        row_sep = QHBoxLayout()
        row_sep.addWidget(QLabel("Séparateur :"))
        row_sep.addWidget(self.sep)
        row_sep.addStretch()
        L.addLayout(row_sep)

        L.addWidget(QLabel("Résultat :"))
        L.addWidget(self.out)
        L.addWidget(self.btn_show)

        row_score = QHBoxLayout()
        row_score.addWidget(self.lbl_score)
        row_score.addWidget(self.meter)
        L.addLayout(row_score)

        row_btns = QHBoxLayout()
        row_btns.addWidget(self.btn_generate)
        row_btns.addWidget(self.btn_copy)
        row_btns.addStretch()
        row_btns.addWidget(self.btn_ok)
        L.addLayout(row_btns)

        # ----- Connexions -----
        self.btn_generate.clicked.connect(self.generate)
        self.btn_copy.clicked.connect(self.copy_out)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_show.stateChanged.connect(self.toggle_echo)
        self.out.textChanged.connect(self.update_score)

        self.generate()

    # ----- Méthodes -----
    def toggle_echo(self, _):
        self.out.setEchoMode(
            QLineEdit.Normal if self.btn_show.isChecked() else QLineEdit.Password
        )

    def copy_out(self):
        QGuiApplication.clipboard().setText(self.out.text())

    def _rand_password(self) -> str:
        alphabet = ""
        if self.cb_lower.isChecked():   alphabet += string.ascii_lowercase
        if self.cb_upper.isChecked():   alphabet += string.ascii_uppercase
        if self.cb_digits.isChecked():  alphabet += string.digits
        if self.cb_symbols.isChecked(): alphabet += "!@#$%^&*()-_=+[]{};:,.?/"
        if self.cb_ambig.isChecked():
            for ch in "l1I|O0":
                alphabet = alphabet.replace(ch, "")
        if not alphabet:
            alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(self.spin_len.value()))

    def _rand_passphrase(self) -> str:
        sep = self.sep.text() or "-"
        return sep.join(secrets.choice(DEFAULT_WORDS) for _ in range(self.spin_words.value()))

    def generate(self):
        pwd = self._rand_passphrase() if self.rb_phrase.isChecked() else self._rand_password()
        self.out.setText(pwd)

    def update_score(self):
        pw = self.out.text()
        if not pw:
            self.meter.setValue(0)
            self.lbl_score.setText("Score : –")
            return
        data = strength(pw)
        sc   = int(data["score"])
        self.meter.setValue(sc)
        self.lbl_score.setText(
            f"Score : {score_to_label(sc)} — {data['crack_times_display']['offline_fast_hashing_1e10_per_second']}"
        )