# PassCode 🔐

Application de quiz en kiosque sécurisé pour l'apprentissage du code de la route français. L'interface est verrouillée au niveau du système d'exploitation pour empêcher l'accès à d'autres fonctionnalités pendant le test.

---

# ⚖️ Informations légales

## Notice légale importante — Statut du contenu en cours de clarification

**PassCode est un projet indépendant, non officiel, et n'est ni développé, ni édité, ni approuvé, ni affilié à l'État français, au Ministère de l'Intérieur, à la Gendarmerie Nationale ou à toute administration publique.**

Seules les **questions et réponses du quiz** ("Je repasse le code") affichées dans l'application sont reprises d'une source publique :

- **Contenu réutilisé** : Questions et réponses du quiz "Je repasse le code"
- **Source du contenu** : https://www.securite-routiere.gouv.fr/les-medias/nos-quiz/je-repasse-le-code
- **Éditeur/propriétaire du contenu source** : Gouvernement français — Délégation à la sécurité routière (PassCode lui-même n'est pas édité par cet organisme)

### Statut du droit d'auteur : en cours de vérification

Ce projet supposait initialement que ce contenu était couvert par la **Licence Ouverte 2.0**, qui autorise la réutilisation libre sous simple attribution. **Cette hypothèse s'est révélée incertaine** : il est possible que ces questions soient en réalité protégées par le droit d'auteur classique, sans réutilisation libre automatique.

**Une demande d'autorisation de réutilisation a été envoyée à la Délégation à la sécurité routière.** Tant qu'une réponse officielle n'a pas été obtenue :

- Le statut juridique exact du contenu du quiz reste **incertain**
- Ce dépôt ne doit pas être considéré comme ayant une autorisation confirmée de réutilisation
- **Aucune release (exécutable, installateur) de PassCode ne sera publiée avant l'obtention de cette autorisation** — seul le code source est disponible dans ce dépôt
- Cette section sera mise à jour dès réception d'une réponse (autorisation, refus, ou conditions spécifiques)

Contenu original : © Gouvernement français — Délégation à la sécurité routière
Source : https://www.securite-routiere.gouv.fr

L'application PassCode (code, interface, système de verrouillage) est un développement indépendant qui n'engage que ses auteurs et n'est pas concernée par cette incertitude — seul le contenu du quiz (questions/réponses/médias) l'est.

## Conditions d'utilisation

1. **Statut du contenu du quiz**
   - Le statut juridique du contenu (questions/réponses) est **en cours de clarification** — voir la [Notice Légale](#notice-légale-importante--statut-du-contenu-en-cours-de-clarification) ci-dessus
   - Une demande d'autorisation a été adressée à la Délégation à la sécurité routière
   - Source : securite-routiere.gouv.fr

2. **Interdictions**
   - ❌ Utilisation malveillante
   - ❌ Contournement des mesures de sécurité
   - ❌ Modification des droits d'auteur

3. **Responsabilité**
   - Cette application est fournie "tel quel"
   - Aucune garantie sur l'exactitude des questions
   - Les questions peuvent être mises à jour par les autorités

## Licence

**Code de PassCode** (application, interface, système de verrouillage) : MIT License (voir fichier `LICENSE`) — propriété de ses auteurs, sans lien avec le Gouvernement français.

**Contenu du quiz réutilisé** (questions/réponses/médias) : statut juridique **en cours de clarification**, voir la [Notice Légale](#notice-légale-importante--statut-du-contenu-en-cours-de-clarification) ci-dessus.
- © Gouvernement français — Délégation à la sécurité routière
- Source : https://www.securite-routiere.gouv.fr
- Une demande d'autorisation de réutilisation a été adressée à la Délégation à la sécurité routière ; ce README sera mis à jour dès réponse.

## Auteur et disclaimer

PassCode est une application de quiz indépendante pour l'apprentissage du code de la route, développée par ses auteurs. Elle réutilise les questions publiées par le Gouvernement français — elle n'est ni développée, ni éditée, ni approuvée par celui-ci.

**Disclaimer** : PassCode n'est **pas** une application officielle et n'est affiliée à aucune administration publique. Le contenu du quiz (questions/réponses) provient d'une source publique dont le statut de réutilisation est en cours de clarification auprès de la Délégation à la sécurité routière ; les droits sur ce contenu restent la propriété du Gouvernement français. Le code de l'application est un développement indépendant.

Pour le vrai test officiel du code de la route : https://www.securite-routiere.gouv.fr/

---

# 👤 Guide utilisateur

Cette partie s'adresse à toute personne souhaitant simplement installer et utiliser PassCode.

## Caractéristiques principales

✨ **Interface plein écran sécurisée**
- Verrouillage complet du clavier (Touche Windows, Alt+Tab, Alt+F4, Ctrl+Alt+Del, etc.)
- Prévention de la fermeture de fenêtre (sauf via le bouton dédié)
- Hook clavier Windows au niveau OS pour un vrai blocage (APIs Windows `SetWindowsHookEx`)

📚 **Quiz mode kiosque**
- Questions aléatoires du code de la route officiel
- Interface responsive avec thème clair/sombre
- Affichage des explications après validation
- Barre de progression en temps réel

🎯 **Configuration flexible**
- Mode de démarrage configurable (boot, déverrouillage)
- Thème persistant (clair/sombre)
- Dataset de questions configurable

🛡️ **Sécurité et robustesse**
- Blocage des raccourcis système au niveau OS
- Nettoyage automatique à la fermeture
- Thread-safe et résistant aux crashes
- Aucun accès au registre Windows pendant le test

## Installation

> ⚠️ **Aucune release n'est publiée pour le moment**, voir les [Informations légales](#-informations-légales) ci-dessus. Les options ci-dessous décrivent l'installation une fois une release disponible.

### Option 1 : Installateur Windows (Recommandé)

1. Téléchargez `PassCode-Setup.exe`
2. Double-cliquez pour lancer l'installation
3. Choisissez les options:
   - ☐ Créer un raccourci sur le bureau
   - ☐ Lancer au démarrage du PC
   - ☐ Lancer à chaque déverrouillage de session
4. Cliquez "Installer"

### Option 2 : Exécutable portable

1. Téléchargez `PassCode.exe`
2. Exécutez directement (aucune installation)

## Utilisation

### Lancer l'application

```bash
PassCode.exe
```

### Interface de quiz

1. **Quiz commence** → L'écran se verrouille automatiquement
2. **Répondre** → Sélectionnez les bonnes réponses (2 sous-questions par question)
3. **Valider** → Cliquez "Valider la réponse"
4. **Voir explication** → Lisez les explications
5. **Continuer** → Cliquez "Question suivante"
6. **Déverrouiller** → Une fois terminé, cliquez "Déverrouiller le PC"

### Options pendant le quiz

- **Bascule thème** → Bouton en haut à droite (🌙/☀️)
- **Barre de progression** → Suit votre avancement
- **Compteur** → Affiche question actuelle / total

## Support et bugs

Pour signaler un bug ou une question:
- Ouvrez une issue sur le dépôt
- Incluez: version Windows, contexte d'utilisation
- Attachez logs si disponible

---

# 🖥️ Guide utilisateur technique

Cette partie s'adresse aux utilisateurs à l'aise en informatique (configuration, format des données, fonctionnement interne), sans nécessiter de compétences en développement.

## Système de verrouillage

### Raccourcis complètement bloqués

| Raccourci | Status |
|-----------|--------|
| Touche Windows | ✅ Bloquée |
| Win+Tab, Win+Esc | ✅ Bloquée |
| Alt+Tab | ✅ Bloquée |
| Alt+F4 | ✅ Bloquée |
| Ctrl+Alt+Del | ✅ Bloquée |
| Esc | ✅ Bloquée |
| F11 | ✅ Bloquée |

### Implémentation

- **Hook clavier global Windows** (`SetWindowsHookEx` via `ctypes`)
- Interception au niveau OS, avant traitement par l'application
- Garantit le blocage même sans focus de fenêtre
- Nettoyage automatique à la fermeture

## Configuration

### app_config.yml

```yaml
nb_questions: 40      # Nombre de questions par session
theme: dark           # Thème par défaut (dark ou light)
```

### dataset.json

Format des questions:

```json
[
  {
    "question_title": "Titre de la question",
    "question_media_name": "image.jpg",
    "question_media_is_image": true,
    "sub_questions": [
      {
        "sub_question": "Question A",
        "choices": [
          {"choice": "Option 1", "is_correct": true},
          {"choice": "Option 2", "is_correct": false}
        ]
      },
      {
        "sub_question": "Question B",
        "choices": [...]
      }
    ],
    "explanations": "Explication de la réponse correcte"
  }
]
```

## Limitations de sécurité

**IMPORTANT**: Ce système est un **contrôle de prévention des accidents**, pas une sécurité robuste.

### ✅ Protection contre

- Fermeture accidentelle
- Raccourcis système
- Alt+Tab, Alt+F4, Ctrl+Alt+Del
- Escape et F11 (sortie plein écran)

### ⚠️ Contournable par

- Démarrage en mode sans échec (Safe Mode), qui ne charge pas les applications de démarrage tierces
- Administrateur système (désinstaller l'app, débrancher le hook)
- Accès physique permettant de démarrer sur un autre support (clé USB, autre disque)

Un simple redémarrage normal du PC **ne suffit pas** à contourner le verrouillage : PassCode se relance automatiquement au démarrage/déverrouillage tant que les options correspondantes sont activées.

## Spécifications

| Élément | Valeur |
|---------|--------|
| Langage | Python 3.14+ |
| UI Framework | PySide6 (Qt 6) |
| Plateforme | Windows 7+ |
| Exe portable | 897 MB |
| Installateur | 1.7 GB |
| Temps démarrage | 2-5 secondes |
| Dépendances embarquées | PySide6, pydantic, PyYAML |

---

# 👨‍💻 Guide développeur

Cette partie s'adresse à celles et ceux qui veulent contribuer au code, comprendre l'architecture, ou builder le projet.

## Architecture

```
RoadCodeLock/
├── src/
│   ├── app/
│   │   ├── app.py                   # Application principale (PySide6)
│   │   ├── keyboard_blocker.py      # Hook clavier Windows
│   │   ├── startup_manager.py       # Gestion des options de démarrage
│   │   ├── config_model.py          # Modèle de configuration
│   │   └── windows_registry_blocker.py  # Blocage registre (optionnel)
│   ├── common/
│   │   └── paths.py                 # Chemins des ressources
│   ├── models/
│   │   └── question_model.py        # Modèle de données du quiz
│   └── scraper/                     # Scraper (non inclus dans exe)
├── assets/
│   ├── styles/                      # Thèmes QSS (clair/sombre)
│   ├── dataset.json                 # Questions du quiz
│   └── uniques_medias/              # Images/vidéos des questions
├── configs/
│   └── app_config.yml               # Configuration par défaut
├── build_tools/
│   ├── build.py / build.ps1         # Scripts de build
│   ├── passcode.spec                # Config PyInstaller
│   └── PassCode.iss                 # Config Inno Setup
└── dist/
    ├── PassCode.exe                 # Exécutable portable (897 MB)
    └── PassCode-Setup.exe           # Installateur Windows (1.7 GB)
```

## Build et déploiement

### Créer les fichiers installable

```bash
# Installer les outils (une seule fois)
pip install pyinstaller
# Télécharger Inno Setup: https://jrsoftware.org/isdl.php

# Créer exe + installateur
python build_tools/build.py

# Résultats
# dist/PassCode.exe              (897 MB - portable)
# dist/PassCode-Setup.exe        (1.7 GB - installateur)
```

Voir [BUILD_GUIDE.md](BUILD_GUIDE.md) pour plus de détails.

## Dépendances

### Runtime (embarquées dans exe)

```
PySide6>=6.11.2      - Interface graphique Qt
pydantic>=2.13.4     - Validation données
PyYAML>=6.0.3        - Configuration YAML
```

### Développement (non embarquées)

```
PyInstaller          - Création executable
Inno Setup           - Installateur Windows
uv                   - Gestionnaire paquets
```

### Scraper uniquement (non inclus exe)

```
Playwright>=1.62.0   - Automation navigateur
beautifulsoup4       - Parsing HTML
ffmpeg-python        - Conversion médias
selectolax>=0.4.11   - Parsing CSS
```

## Contribution

Les contributions sont bienvenues! Pour:
- Signaler un bug
- Proposer une amélioration
- Ajouter des questions
- Corriger des traductions

Créez une issue ou PR.
