# Système de Verrouillage du Clavier - RoadCodeLock

## Vue d'ensemble

Le système de verrouillage du clavier empêche l'utilisateur d'interagir avec le système d'exploitation en dehors de l'application RoadCodeLock. Il verrouille :

- **Les raccourcis système** — Win, Alt+Tab, Alt+F4, Ctrl+Alt+Del, F11, Esc
- **La fermeture de fenêtre** — La fenêtre ne peut être fermée que via le bouton "Déverrouiller le PC"

## Architecture

### Fichiers principaux

```
src/app/
├── keyboard_blocker.py     # Module de verrouillage du clavier (API Windows)
├── app.py                  # Intégration du verrouillage
└── ...
```

### Composants

#### 1. `keyboard_blocker.py` — Hook global Windows

Utilise les **APIs Windows** (`SetWindowsHookEx`) pour intercepter les événements clavier au niveau du système d'exploitation.

**Classe principale : `KeyboardBlocker`**

- **Mécanisme** : Hook global clavier (`WH_KEYBOARD_LL`)
  - Intercepte TOUS les événements clavier avant traitement OS
  - Bloque au niveau système, pas au niveau application
  - Fonctionne même si la fenêtre n'a pas le focus

- **Raccourcis bloqués**
  - Win (touche Windows seule)
  - Win+Esc, Win+Tab
  - Alt+Tab, Alt+F4
  - Ctrl+Alt+Del
  - F11 (plein écran)
  - Esc seul

- **Méthodes publiques**
  - `lock()` → bool — Active le verrouillage, retourne True/False
  - `unlock()` → bool — Désactive le verrouillage, retourne True/False
  - `locked()` — Context manager pour verrouillage temporaire

- **Callbacks internes**
  - `_keyboard_hook()` — Callback du hook Windows (très bas niveau)
  - `_should_block_key()` — Détermine si une touche doit être bloquée
  - `_is_alt_pressed()` / `_is_ctrl_pressed()` — Vérifient les touches modificatrices

**Fonctions module**

- `get_keyboard_blocker()` — Obtient l'instance globale (singleton)
- `lock_keyboard()` → bool — Verrouille globalement
- `unlock_keyboard()` → bool — Déverrouille globalement

#### 2. `app.py` (modifications)

Intègre le verrouillage dans la fenêtre principale.

**Modifications**

- Import `QCloseEvent` et fonctions `lock_keyboard()`, `unlock_keyboard()`
- Ajout d'un attribut `_allow_close` dans `__init__`
- Appel de `lock_keyboard()` après initialisation de l'UI
- Modification du bouton "Déverrouiller le PC" pour appeler `_close()` au lieu de `close()`
- Ajout d'une méthode `_close()` qui autorise la fermeture
- Ajout d'une méthode `closeEvent()` qui :
  - Refuse la fermeture si `_allow_close` est False
  - Appelle `unlock_keyboard()` avant de fermer

## Flux de démarrage et fermeture

### Démarrage

```
main()
  ↓
QApplication()
  ↓
Window.__init__()
  ├─ init_ui()
  ├─ apply_theme()
  ├─ set_question()
  └─ lock_keyboard()  ← Installe hook Windows
  ↓
window.show()
  ↓
Application démarre avec clavier verrouillé
```

### Fermeture (via bouton "Déverrouiller le PC")

```
Utilisateur clique "Déverrouiller le PC"
  ↓
_close()
  ├─ _allow_close = True
  └─ close()
  ↓
closeEvent()
  ├─ Vérifie _allow_close (True)
  ├─ unlock_keyboard()  ← Désinstalle hook Windows
  └─ Ferme la fenêtre
  ↓
atexit hook
  └─ Appel automatique de unlock()
  ↓
Application se termine
```

### Tentative de fermeture non autorisée

```
Utilisateur appuie sur Alt+F4 / Win / etc.
  ↓
Hook Windows intercepte l'événement
  ↓
_keyboard_hook() appelée par l'OS
  ↓
_should_block_key() retourne True
  ↓
Fonction hook retourne 1 (bloque l'événement)
  ↓
L'OS consume l'événement et ne le traite pas
```

## Raccourcis système bloqués

| Raccourci | Code | Description |
|-----------|------|-------------|
| **Win** | 0x5B (VK_LWIN) / 0x5C (VK_RWIN) | Touche Windows seule |
| **Alt+Tab** | VK_TAB + VK_ALT | Sélecteur de tâches |
| **Alt+F4** | VK_F4 + VK_ALT | Fermer la fenêtre |
| **Ctrl+Alt+Del** | VK_DELETE + VK_CTRL + VK_ALT | Écran de verrouillage Windows |
| **Esc** | 0x1B (VK_ESCAPE) | Escape (sortie plein écran) |
| **F11** | 0x7A (VK_F11) | Plein écran / Sortie plein écran |

## Détails techniques

### Hook clavier Windows (SetWindowsHookEx)

```c
// Signature C
LRESULT CALLBACK KeyboardProc(
  int    nCode,      // Code du hook
  WPARAM wParam,     // Type d'événement (WM_KEYDOWN, WM_KEYUP, etc.)
  LPARAM lParam      // Pointeur à KBDLLHOOKSTRUCT
);

// Installation
HHOOK hHook = SetWindowsHookExW(
  WH_KEYBOARD_LL,    // Type de hook (clavier low-level)
  KeyboardProc,      // Pointeur à la fonction callback
  NULL,              // DLL (NULL = même processus)
  0                  // ID du thread (0 = tous les threads)
);
```

### Structure KBDLLHOOKSTRUCT

```python
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", c_uint32),      # Code de touche virtuelle
        ("scanCode", c_uint32),    # Scan code
        ("flags", c_uint32),       # Flags (injecté, étendu, etc.)
        ("time", c_uint32),        # Timestamp
        ("dwExtraInfo", c_void_p), # Info supplémentaire
    ]
```

### Codes d'événements clavier

| Constante | Valeur | Description |
|-----------|--------|-------------|
| WM_KEYDOWN | 0x0100 | Touche pressée (normal) |
| WM_KEYUP | 0x0101 | Touche relâchée (normal) |
| WM_SYSKEYDOWN | 0x0104 | Touche système pressée (Alt+X) |
| WM_SYSKEYUP | 0x0105 | Touche système relâchée (Alt+X) |

### Codes de touches virtuelles (sélection)

```
VK_LWIN = 0x5B         # Windows gauche
VK_RWIN = 0x5C         # Windows droit
VK_TAB = 0x09          # Tab
VK_F4 = 0x73           # F4
VK_DELETE = 0x46       # Del
VK_ESCAPE = 0x1B       # Esc
VK_F11 = 0x7A          # F11
VK_LALT = 0xA4         # Alt gauche
VK_RALT = 0xA5         # Alt droit
VK_LCTRL = 0xA2        # Ctrl gauche
VK_RCTRL = 0xA3        # Ctrl droit
```

### Retours de la callback

| Valeur | Signification |
|--------|---------------|
| 0 | Événement passé au hook suivant (traité normalement) |
| 1 | Événement consommé (BLOQUÉ, ne sera pas traité) |

### Thread-safety

Utilise un `threading.Lock` pour synchroniser l'accès à `pressed_keys` :

```python
with self._lock:
    self.pressed_keys.add(vk_code)
    if self._should_block_key(vk_code):
        return 1  # Bloque
```

### Nettoyage à la fermeture

Enregistre un hook `atexit` pour garantir le déverrouillage même en cas de crash :

```python
atexit.register(self.unlock)
```

## Limitations et considérations

### ✅ Ce qui fonctionne

- ✓ Bloque les raccourcis système au niveau de l'OS
- ✓ Fonctionne même sans focus de fenêtre
- ✓ Empêche la fermeture accidentelle ou intentionnelle
- ✓ Garantit le déverrouillage à la fermeture de l'application
- ✓ Thread-safe et robuste aux crashes
- ✓ Vrai blocage (not just ignoring input at app level)

### ⚠️ Limitations

1. **Windows uniquement** — Utilise les APIs Windows directes
   - Non portable sur Linux/macOS
   - Nécessite Python sur Windows

2. **Clavier virtuel** — Un clavier virtuel (écran tactile) ne serait pas bloqué
   - Ce système cible uniquement le clavier physique/USB

3. **Niveau utilisateur** — Basé sur les APIs utilisateur, pas noyau
   - Un utilisateur avec droits administrateur peut débrancher le hook
   - Un processus noyau peut contourner les APIs utilisateur

4. **Processus externes** — Certains programmes système peuvent ignorer le hook
   - Programmes avec SYSTEM privilege
   - Drivers noyau

### 🔒 Sécurité

**Important** : Ce système est un **contrôle de prévention des accidents**, pas une **sécurité robuste**. Un utilisateur déterminé peut contourner :

- **Redémarrage forcé** — Ctrl+Alt+Del → écran de verrouillage
- **Accès disque** — Boot sur clé USB, modification de l'installation
- **Process manipulation** — Task Manager (si droits admin)
- **Logiciel de contournement** — Driver noyau personnalisé

**Pour une véritable sécurité** : considérez
- Kiosque mode Windows (confinement OS-level)
- UEFI Secure Boot + signature de drivers
- Supervision physique
- Écran tactile uniquement + pas d'USB
- VT-x/AMD-V avec hypervisor (virtualisation)

## Installation et utilisation

### Installation des dépendances

```bash
uv sync
```

Aucune dépendance externe supplémentaire n'est nécessaire au-delà de ce qui est déjà dans `pyproject.toml` (les APIs Windows sont fournies par `ctypes`, stdlib).

### Lancement de l'application

```bash
uv run python src/app/app.py
```

L'application démarre en plein écran avec le clavier verrouillé.

### Déverrouillage

Cliquez sur le bouton "Déverrouiller le PC" en bas de l'écran après complétion du quiz.

### Vérification

Une fois verrouillé, testez que :
- ✓ Touche Windows n'ouvre pas le menu Démarrage
- ✓ Alt+Tab ne bascule pas les fenêtres
- ✓ Alt+F4 ne ferme pas la fenêtre
- ✓ Esc ne sort pas du plein écran
- ✓ F11 ne bascule pas le plein écran

## Débogage

### Activer les logs

Modifiez `keyboard_blocker.py` pour ajouter des logs :

```python
def _keyboard_hook(self, nCode, wParam, lParam):
    print(f"Hook appelée: code={nCode}, event={wParam}")
    # ... reste du code
```

### Vérifier que le hook est installé

```python
from src.app.keyboard_blocker import get_keyboard_blocker

blocker = get_keyboard_blocker()
print(f"Verrouillé : {blocker.is_locked}")
print(f"Handle du hook : {blocker.hook_handle}")
```

### Tester le verrouillage isolément

```python
from src.app.keyboard_blocker import lock_keyboard, unlock_keyboard
import time

print("Verrouillage...")
lock_keyboard()
print("Testez Alt+Tab, Win, Alt+F4... (5 secondes)")
time.sleep(5)

print("Déverrouillage...")
unlock_keyboard()
print("Maintenant les raccourcis fonctionnent à nouveau!")
```

## Différences avec la version précédente

| Aspect | Ancienne version (pynput) | Nouvelle version (ctypes) |
|--------|--------------------------|--------------------------|
| **Mécanisme** | Listener d'événements pynput | Hook clavier Windows API |
| **Niveau** | Application (event listener) | Système d'exploitation (low-level hook) |
| **Fiabilité** | Modérée (contournable) | Très élevée (bloque complètement) |
| **Focus requis** | Oui (fenêtre doit avoir focus) | Non (fonctionne globalement) |
| **Dépendance** | pynput | Aucune (ctypes = stdlib) |
| **Portabilité** | Unix/Windows/macOS | Windows uniquement |

## Références

- [SetWindowsHookEx - MSDN](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowshookexw)
- [Virtual Key Codes - MSDN](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes)
- [Keyboard Input - MSDN](https://learn.microsoft.com/en-us/windows/win32/inputdev/keyboard-input)
- [ctypes documentation - Python](https://docs.python.org/3/library/ctypes.html)
