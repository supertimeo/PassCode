# Module de Blocage Registre Windows - RoadCodeLock

## ⚠️ Attention

Ce module modifie le registre Windows et nécessite **les droits administrateur**. Il est **optionnel** et fourni pour une protection supplémentaire des raccourcis système.

**Utilisez-le uniquement si vous comprenez les implications et êtes conscient du risque.**

## Vue d'ensemble

Le module `windows_registry_blocker.py` ajoute une **couche supplémentaire** de protection en bloquant les raccourcis système au niveau du registre Windows.

### Différence avec le `keyboard_blocker.py`

| Aspect | keyboard_blocker.py | windows_registry_blocker.py |
|--------|-------------------|---------------------------|
| **Mécanisme** | Interception d'événements clavier | Modification du registre Windows |
| **Niveau** | Application | Système d'exploitation |
| **Droits** | Aucun requis | Admin requis |
| **Fiabilité** | Haute (mais contournable) | Très haute (système-level) |
| **Activation** | Automatique | Manuelle (optionnel) |
| **Restauration** | Automatique à la fermeture | Manuelle ou au redémarrage |

## Raccourcis bloqués via registre

| Raccourci | Paramètre registre | Impact |
|-----------|------------------|--------|
| **Alt+Tab** | `DisableAltTab` | Impossible de basculer entre fenêtres |
| **Ctrl+Alt+Del** | `DisableCtrlAltDel` | Impossible d'accéder à l'écran de verrouillage |
| **Win+L** | `DisableLockWorkstation` | Impossible de verrouiller le PC via clavier |
| **Win** | `NoWinKeys` | Touche Windows complètement désactivée |

## Installation

Aucune dépendance supplémentaire n'est nécessaire. Le module utilise `winreg` (stdlib Python).

## Utilisation

### Option 1 : Utilisation indépendante

```python
from src.app.windows_registry_blocker import WindowsRegistryBlocker

# Créer une instance
blocker = WindowsRegistryBlocker()

# Vérifier les droits admin
if not blocker._is_admin():
    print("Erreur : Droits admin requis")
    exit(1)

# Bloquer les raccourcis système
if blocker.enable():
    print("Raccourcis système bloqués")
    # ... utiliser l'application ...
else:
    print("Erreur lors du blocage")

# Restaurer les paramètres originaux
if blocker.disable():
    print("Paramètres restaurés")
```

### Option 2 : Utilisation avec l'app principale (recommandée)

**Modification d'app.py pour inclure le blocage optionnel :**

```python
# Au début du fichier
import os
from app.keyboard_blocker import lock_keyboard, unlock_keyboard
from app.windows_registry_blocker import enable_registry_blocking, disable_registry_blocking

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... code existant ...
        
        # Optionnel : Vérifier si on doit activer le blocage registre
        # Définir la variable d'environnement USE_REGISTRY_BLOCKER=1
        if os.environ.get("USE_REGISTRY_BLOCKER", "0") == "1":
            if enable_registry_blocking():
                print("✓ Blocage registre activé")
            else:
                print("✗ Impossible d'activer le blocage registre (admin requis?)")

    def closeEvent(self, event: QCloseEvent):
        if not self._allow_close:
            event.ignore()
            return

        unlock_keyboard()
        
        # Restaurer les paramètres registre si activés
        if os.environ.get("USE_REGISTRY_BLOCKER", "0") == "1":
            disable_registry_blocking()
        
        event.accept()
```

### Option 3 : Utilisation en ligne de commande

```bash
# Windows PowerShell (avec droits admin)
$env:USE_REGISTRY_BLOCKER="1"
uv run python src/app/app.py

# Ou CMD
set USE_REGISTRY_BLOCKER=1
uv run python src/app/app.py
```

## Considérations de sécurité

### ✅ Avantages

- **Niveau système** — Bloque les raccourcis au niveau de l'OS, pas seulement l'app
- **Complémentaire** — Fonctionne en tandem avec `keyboard_blocker.py`
- **Restauration garantie** — Le code enregistre et restaure les paramètres originaux

### ⚠️ Risques

1. **Droits administrateur** — Modifie le registre système
2. **Dysfonctionnement potentiel** — Si restauration échoue, les raccourcis restent bloqués
3. **Incompatibilité** — Certaines versions de Windows ou configurations peuvent rejeter les modifications
4. **Détection d'antivirus** — Certains AV détectent les modifications du registre

### 🔒 Contournements possibles

Même avec ce blocage :
- Un utilisateur peut redémarrer le PC (saute la restauration)
- Accès physique à la machine : arrêt forcé, reformatage
- Modifications manuelles du registre avec autre outil
- Boot sur une clé USB/live USB

## Dépannage

### Erreur : "Droits administrateur requis"

```
Erreur : Les droits administrateur sont nécessaires pour modifier le registre.
Lancez l'application en tant qu'administrateur.
```

**Solution :**

1. Faites un clic droit sur cmd.exe ou PowerShell
2. Choisir "Exécuter en tant qu'administrateur"
3. Naviguer vers le dossier du projet
4. Lancer : `uv run python src/app/app.py`

### Raccourcis reste bloqués après fermeture

Si l'application crash ou se ferme anormalement, les paramètres registre peuvent rester bloqués.

**Solution manuelle :**

1. Ouvrir le Registre (Win+R, taper `regedit`)
2. Naviguer vers : `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System`
3. Supprimer ou modifier les clés :
   - `DisableAltTab` → Supprimer (ou mettre à 0)
   - `DisableCtrlAltDel` → Supprimer (ou mettre à 0)
   - `DisableLockWorkstation` → Supprimer (ou mettre à 0)
   - `NoWinKeys` → Supprimer (ou mettre à 0)
4. Redémarrer l'ordinateur

**Solution via script PowerShell (admin) :**

```powershell
$path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\System"
if (Test-Path $path) {
    Remove-ItemProperty -Path $path -Name "DisableAltTab" -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $path -Name "DisableCtrlAltDel" -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $path -Name "DisableLockWorkstation" -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $path -Name "NoWinKeys" -ErrorAction SilentlyContinue
    Write-Host "Paramètres restaurés"
}
```

## Recommandations

1. **Mode kiosque** — Pour une protection réelle, utilisez le mode Kiosque Windows
2. **Supervision** — L'utilisateur doit être supervisé
3. **Sans dépendances externes** — N'installez pas de logiciels durant le test
4. **Test préalable** — Testez toujours d'abord en environnement contrôlé
5. **Logging** — Enregistrez les tentatives de contournement

## Références

- [Políticas de Seguridad en Windows](https://learn.microsoft.com/en-us/windows/client-management/mdm/)
- [Registry Keys for Application Management](https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-elements-for-grouping-and-priority)
- [Windows Kiosk Mode](https://learn.microsoft.com/en-us/windows/configuration/kiosk-mode)
