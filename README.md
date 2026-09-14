# PassCode 🔐

Application de quiz en kiosque sécurisé pour l'apprentissage du code de la route français. L'interface est verrouillée au niveau du système d'exploitation pour empêcher l'accès à d'autres fonctionnalités pendant le test.

## ⚠️ Notice Légale Importante

**Cette application utilise du contenu public provenant de securite-routiere.gouv.fr**

- **Contenu utilisé**: Questions et réponses du quiz "Je repasse le code"
- **Source**: https://www.securite-routiere.gouv.fr/les-medias/nos-quiz/je-repasse-le-code
- **Licence**: Licence Ouverte 2.0 (Open Licence)
- **Organisme public**: Ministère de l'Intérieur - Direction générale de la Gendarmerie Nationale
- **Attribution requise**: Oui

### Attribution

Cette application réutilise le contenu pédagogique officiel du Gouvernement français sous la **Licence Ouverte 2.0**. 

Données originales: © Gouvernement français - Ministère de l'Intérieur - Direction générale de la Gendarmerie Nationale
Source: https://www.securite-routiere.gouv.fr

### Licence Ouverte 2.0

Vous êtes libres de:
- ✅ Réutiliser les contenus
- ✅ Adapter et transformer
- ✅ Utiliser à titre commercial ou non-commercial

Sous condition de:
- 🏷️ **Mention de la source obligatoire** (Gouvernement français)
- 🔗 **Lien vers la Licence Ouverte 2.0** (http://www.etalab.gouv.fr/licence-ouverte-open-licence)

Pour plus d'informations: http://www.etalab.gouv.fr/

## 📋 Caractéristiques principales

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

## 🚀 Installation

### Option 1 : Installateur Windows (Recommandé)

1. Téléchargez `PassCode-Setup.exe`
2. Double-cliquez pour lancer l'installation
3. Choisissez les options:
   - ☐ Créer un raccourci sur le bureau
   - ☐ Lancer au démarrage du PC
4. Cliquez "Installer"

### Option 2 : Exécutable portable

1. Téléchargez `PassCode.exe`
2. Exécutez directement (aucune installation)

### Option 3 : Depuis le code source

```bash
cd RoadCodeLock
uv sync
uv run python src/app/app.py
```

## 📖 Utilisation

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

## 🔒 Système de verrouillage

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

## 🏗️ Architecture

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

## ⚙️ Configuration

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

## 🔧 Build et déploiement

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

## 🔐 Limitations de sécurité

**IMPORTANT**: Ce système est un **contrôle de prévention des accidents**, pas une sécurité robuste.

### ✅ Protection contre

- Fermeture accidentelle
- Raccourcis système
- Alt+Tab, Alt+F4, Ctrl+Alt+Del
- Escape et F11 (sortie plein écran)

### ⚠️ Contournable par

- Redémarrage du PC (Ctrl+Alt+Suppr)
- Administrateur système (débrancher le hook)
- Accès physique (redémarrage, changement disque)

### 🔒 Pour une vraie sécurité

Considérez:
- Windows Kiosk Mode (verrouillage OS-level)
- UEFI Secure Boot
- Supervision physique
- Écran tactile uniquement
- Virtualisation (hypervisor)

## 📊 Spécifications

| Élément | Valeur |
|---------|--------|
| Langage | Python 3.14+ |
| UI Framework | PySide6 (Qt 6) |
| Plateforme | Windows 7+ |
| Exe portable | 897 MB |
| Installateur | 1.7 GB |
| Temps démarrage | 2-5 secondes |
| Dépendances embarquées | PySide6, pydantic, PyYAML |

## 📝 Dépendances

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

## 🤝 Contribution

Les contributions sont bienvenues! Pour:
- Signaler un bug
- Proposer une amélioration
- Ajouter des questions
- Corriger des traductions

Créez une issue ou PR.

## ⚖️ Conditions d'utilisation

1. **Respect de la Licence Ouverte 2.0**
   - Attribution du Gouvernement français obligatoire
   - Source: securite-routiere.gouv.fr

2. **Interdictions**
   - ❌ Utilisation malveillante
   - ❌ Contournement des mesures de sécurité
   - ❌ Modification des droits d'auteur

3. **Responsabilité**
   - Cette application est fournie "tel quel"
   - Aucune garantie sur l'exactitude des questions
   - Les questions peuvent être mises à jour par les autorités

## 📞 Support et bugs

Pour signaler un bug ou une question:
- Ouvrez une issue sur le dépôt
- Incluez: version Windows, contexte d'utilisation
- Attachez logs si disponible

## 📜 Licence

**Code**: MIT License (voir fichier `LICENSE`)

**Contenu pédagogique**: Licence Ouverte 2.0 - Gouvernement français
- © Ministère de l'Intérieur
- Source: https://www.securite-routiere.gouv.fr

## 👨‍💻 Auteur

PassCode - Application de quiz sécurisé pour l'apprentissage du code de la route

Réutilisation du contenu pédagogique officiel français sous Licence Ouverte 2.0

---

**Disclaimer**: Cette application n'est pas officielle. C'est une réutilisation du contenu public selon la Licence Ouverte 2.0. Le contenu reste la propriété du Gouvernement français.

Pour plus d'informations sur le vrai test du code de la route: https://www.securite-routiere.gouv.fr/
