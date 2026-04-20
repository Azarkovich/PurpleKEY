# PurpleKEY

Gestionnaire de mots de passe local, chiffré et open source.

## Fonctionnalités

- Chiffrement AES-256-GCM avec dérivation de clé Argon2id
- Architecture zéro-connaissance — vos données ne quittent jamais votre machine
- Générateur de mots de passe intégré (aléatoire ou passphrase)
- Évaluation de la force des mots de passe
- Système de favoris
- Recherche en temps réel
- Deux backends de stockage : fichier CBOR ou SQLite

## Téléchargement

| Plateforme | Lien |
|------------|------|
| Linux | [PurpleKEY-linux](https://github.com/Azarkovich/PurpleKEY/releases/latest/download/PurpleKEY-linux) |
| Windows | [PurpleKEY-windows.exe](https://github.com/Azarkovich/PurpleKEY/releases/latest/download/PurpleKEY-windows.exe) |
| macOS | [PurpleKEY-macos](https://github.com/Azarkovich/PurpleKEY/releases/latest/download/PurpleKEY-macos) |

## Installation

### Linux / macOS

```bash
chmod +x PurpleKEY-linux
./PurpleKEY-linux
```

### Windows

Double-cliquez sur `PurpleKEY-windows.exe`.

## Première utilisation

1. Lancez l'application
2. Cliquez **"Première fois ? Créer un coffre"**
3. Choisissez un mot de passe maître fort. **il est impossible de le récupérer en cas d'oubli**
4. Ajoutez vos entrées

## Sécurité

| Composant | Détail |
|-----------|--------|
| Chiffrement | AES-256-GCM |
| Dérivation de clé | Argon2id (64 MB RAM, 3 itérations) |
| Stockage | CBOR binaire chiffré |
| Vérification | Tag GCM — pas de hash stocké |

Le coffre est stocké localement dans le répertoire utilisateur. Aucune donnée n'est envoyée sur internet.

## Stack technique

- Python 3.11
- PySide6 — interface graphique
- cryptography — AES-256-GCM
- argon2-cffi — dérivation de clé
- cbor2 — sérialisation binaire
- zxcvbn — évaluation de force

## Développement

```bash
git clone https://github.com/Azarkovich/PurpleKEY.git
cd PurpleKEY
pip install -r requirements.txt
python main.py
```

## Auteur

Xavier TOKO-PROUST — [azar-security.site](https://azar-security.site) · [GitHub](https://github.com/Azarkovich)