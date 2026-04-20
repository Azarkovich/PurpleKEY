#services/strength.py

"""
    Évaluation de la force d'un mot de passe via zxcvbn
"""

# ----- IMPORT ----- 
from zxcvbn import zxcvbn


def strength(password: str) -> dict:
    return zxcvbn(password)

def score_to_label(score: int) -> str:
    return ["Très faible", "Faible", "Moyen", "Fort", "Très fort"][score]