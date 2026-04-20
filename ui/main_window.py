#ui/main_window.py

"""
    Fenêtre principal
"""

# ----- IMPORTS ----- 
from PySide6.QtWidgets      import (
    QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QPushButton, QLineEdit,
    QListWidget, QInputDialog, QApplication,
    QMessageBox
)
from PySide6.QtCore         import Qt
from PySide6.QtGui          import QGuiApplication

from ui.theme               import *
from core.models            import Entry


class MainWindow(QMainWindow):
    def __init__(self, vault):
        super().__init__()
        self.vault              = vault
        self._entries           = []    # liste des Entry, synchronisée avec list_widget
        self._current_filter    = "all"
        self.setWindowTitle("PurpleKEY")
        self.setMinimumSize(900, 600)
        self.resize(900, 600)
        self.setStyleSheet(f"background-color: {BG_DEEP};")
    
        # Widget Central
        central = QWidget()
        central.setStyleSheet(f"background-color: {BG_DEEP};")
        self.setCentralWidget(central)

        # layout
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(160)
        sidebar.setStyleSheet(f"background-color: {BG_DARK}; border-right: 1px solid {BORDER};")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 16, 8, 16)
        sidebar_layout.setSpacing(2)

       
        def make_side_btn(text, active=False):
            btn = QPushButton(text)
            btn.setFlat(True)
            btn.setFixedHeight(28)
            btn.setCursor(Qt.PointingHandCursor)
            color = VIOLET_LT if active else TEXT_MUT
            bg = f"background-color: {BG_HOVER};" if active else "background: transparent;"
            btn.setStyleSheet(f"""
                QPushButton {{
                    {bg}
                    color: {color};
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                    text-align: left;
                    padding: 0 8px;
                }}
                QPushButton:hover {{
                    background-color: {BG_HOVER};
                    color: {VIOLET_LT};
                }}
            """)
            return btn
        

        # ----- ONGLETS ----- 
        self.btn_all = make_side_btn("Tout", active=True)
        self.btn_favs = make_side_btn("Favoris")

        sidebar_layout.addWidget(self.btn_all)
        sidebar_layout.addWidget(self.btn_favs)

        sidebar_layout.addStretch()

        btn_lock = make_side_btn("Verrouiller")
        btn_lock.setStyleSheet(btn_lock.styleSheet().replace(TEXT_MUT, DANGER))
        sidebar_layout.addWidget(btn_lock)

        main_layout.addWidget(sidebar)

        # ----- ZONE CONTENU -----
        content = QWidget()
        content.setStyleSheet(f"background-color: {BG_DEEP};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        main_layout.addWidget(content)


        # ----- TOPBAR -----
        topbar = QWidget()
        topbar.setFixedHeight(52)
        topbar.setStyleSheet(f"background-color: {BG_DARK}; border-bottom: 1px solid {BORDER};")

        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(16, 0, 16, 0)
        topbar_layout.setSpacing(10)

        # Champ de recherche
        self.search = QLineEdit()
        self.search.setPlaceholderText("Rechercher...")
        self.search.setFixedHeight(32)
        self.search.setStyleSheet(f"""
            QLineEdit {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_LT};
                border-radius: 6px;
                color: {TEXT_PRI};
                font-size: 13px;
                padding: 0 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {VIOLET};
            }}
        """)

        # Bouton Ajouter
        self.btn_add = QPushButton("+ Ajouter")
        self.btn_add.setFixedSize(100, 32)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setStyleSheet(f"""
            QPushButton {{
                background-color: {VIOLET};
                color: {VIOLET_XLT};
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: #6d28d9; }}
            QPushButton:pressed {{ background-color: #5b21b6; }}
        """)

        topbar_layout.addWidget(self.search)
        topbar_layout.addWidget(self.btn_add)

        content_layout.addWidget(topbar)


        # Bouton Supprimer
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.setFixedSize(100, 32)
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.setStyleSheet(f"""
            QPushButton {{
                background-color: {DANGER};
                color: #fff;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: #a3203a; }}
        """)
        topbar_layout.addWidget(self.btn_delete)


        # Bouton Modifier
        self.btn_edit = QPushButton("Modifier")
        self.btn_edit.setFixedSize(100, 32)
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.btn_edit.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_HOVER};
                color: {VIOLET_LT};
                border: 1px solid {BORDER_LT};
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: {BG_CARD}; }}
        """)
        topbar_layout.addWidget(self.btn_edit)

        
        # Bouton Favorite
        self.btn_favorite   = QPushButton("★ Favori")
        self.btn_favorite.setFixedSize(100, 32)
        self.btn_favorite.setCursor(Qt.PointingHandCursor)
        self.btn_favorite.setStyleSheet(f"""
            QPushButton {{
                background-color: {BG_HOVER};
                color: {VIOLET_LT};
                border: 1px solid {BORDER_LT};
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: {BG_CARD}; }}
        """)
        topbar_layout.addWidget(self.btn_favorite)
                

        # ----- LISTE DES ENTRÉES -----
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {BG_DEEP};
                border: none;
                padding: 8px;
            }}
            QListWidget::item {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER};
                border-radius: 6px;
                color: {TEXT_PRI};
                font-size: 13px;
                padding: 10px 12px;
                margin-bottom: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {BG_HOVER};
                border: 1px solid {VIOLET};
                color: {VIOLET_XLT};
            }}
            QListWidget::item:hover {{
                background-color: {BG_HOVER};
                border: 1px solid {BORDER_LT};
            }}
        """)

        content_layout.addWidget(self.list_widget)


        # ----- CONNEXIONS -----
        self.btn_add.clicked.connect(self._on_add)
        btn_lock.clicked.connect(self._on_lock)
        self.search.textChanged.connect(self._on_search)
        self.list_widget.itemDoubleClicked.connect(self._on_copy)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_favorite.clicked.connect(self._on_favorite)

        self.btn_all.clicked.connect(lambda: self._set_filter("all"))
        self.btn_favs.clicked.connect(lambda: self._set_filter("favorites"))
        
        self.refresh_list()




    # ----- FONCTIONNALITÉS -----
    def refresh_list(self):
        if self.vault is None:
            return
        
        self.list_widget.clear()
        all_entries = self.vault.list_entries()
        if self._current_filter == "favorites":
            self._entries = [e for e in all_entries if e.is_favorite]
        else:
            self._entries = all_entries
        for entry in self._entries:
            star = "★ " if entry.is_favorite else ""
            self.list_widget.addItem(f"{star}{entry.title} - {entry.username}")


    def _get_selected_entry(self):
        idx = self.list_widget.currentRow()
        if idx < 0 or idx >= len(self._entries):
            return None
        return self._entries[idx]

    def _on_lock(self):
        self.vault.lock()
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow(self.vault)
        self.login_window.show()
        self.close()

    def _on_search(self, query):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(query.lower() not in item.text().lower())

    def _on_add(self):
        if self.vault is None:
            return

        title, ok = QInputDialog.getText(self, "Nouvelle entrée", "Titre / Site :")
        if not ok or not title:
            return

        username, ok = QInputDialog.getText(self, "Nouvelle entrée", "Identifiant :")
        if not ok:
            return

        # Générateur de Mdp
        reply = QMessageBox.question(
            self, "Mot de passe",
            "Voulez-vous générer un mot de passe automatiquement ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            from ui.generator_dialog import GeneratorDialog
            gen = GeneratorDialog(self)
            if gen.exec():
                password = gen.out.text()
            else:
                return
        else:
            password, ok = QInputDialog.getText(self, "Nouvelle entrée", "Mot de passe :")
            if not ok or not password:
                return

        self.vault.add_entry(Entry.new(title, username, password))
        self.refresh_list()


    def _on_copy(self):
        entry = self._get_selected_entry()

        if not entry:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner une entrée")
            return 
        QGuiApplication.clipboard().setText(entry.password)
        QMessageBox.information(self, 'Copié', f"Mot de passe de '{entry.title}' copié.")
        

    def _on_delete(self):
        entry           = self._get_selected_entry()
        if not entry:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner une entrée")
            return 
        reply           = QMessageBox.question(self, "Confirmer", f"Supprimer '{entry.title}' ?", 
                            QMessageBox.Yes | QMessageBox.No)
        if reply        == QMessageBox.Yes:
            self.vault.delete_entry(entry.id)
            self.refresh_list()

    def _on_edit(self):
        entry                   = self._get_selected_entry()
        if not entry:
            QMessageBox.warning(self, "Erreur", "Veuillez selectionner une entrée")
            return
        
        title, ok               = QInputDialog.getText(self, "Modifier", 'Titre :', text=entry.title)
        if not ok or not title:
            return
        
        username, ok            = QInputDialog.getText(self, "Modifier", 'Identifiant :', text=entry.username)
        if not ok or not username:
            return
        
        password, ok            = QInputDialog.getText(self, "Modifier", 'Mot de passe :', text=entry.password)
        if not ok or not password:
            return
        
        self.vault.update_entry(entry.id, title=title, username=username, password=password)
        self.refresh_list()


    def _set_filter(self, filter_name):
        self._current_filter = filter_name

        active   = f"background-color: {BG_HOVER}; color: {VIOLET_LT}; border: none; border-radius: 4px; font-size: 12px; text-align: left; padding: 0 8px;"
        inactive = f"background: transparent; color: {TEXT_MUT}; border: none; border-radius: 4px; font-size: 12px; text-align: left; padding: 0 8px;"

        self.btn_all.setStyleSheet(f"QPushButton {{ {active if filter_name == 'all' else inactive} }}")
        self.btn_favs.setStyleSheet(f"QPushButton {{ {active if filter_name == 'favorites' else inactive} }}")

        self.refresh_list()


    def _on_favorite(self):
        entry = self._get_selected_entry()
        if not entry:
            QMessageBox.warning(self, "Erreur", "Sélectionnez une entrée d'abord.")
            return
        self.vault.update_entry(
            entry.id,
            title       = entry.title,
            username    = entry.username,
            password    = entry.password,
            notes       = entry.notes,
            is_favorite = not entry.is_favorite  # ← bascule
        )
        self.refresh_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(vault=None)
    win.show()
    sys.exit(app.exec())