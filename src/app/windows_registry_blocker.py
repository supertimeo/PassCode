"""
Module optionnel pour bloquer les raccourcis système Windows au niveau du registre.

⚠️ Attention : Ce module modifie le registre Windows et nécessite les droits administrateur.
   Il est optionnel et fourni à titre informatif.

Usage :
    from src.app.windows_registry_blocker import WindowsRegistryBlocker
    blocker = WindowsRegistryBlocker()
    blocker.enable()  # Bloque les raccourcis système
    # ... utiliser l'application ...
    blocker.disable()  # Restaure les paramètres originaux
"""


import contextlib
import sys
import winreg
from typing import Optional, cast


class WindowsRegistryBlocker:
    """Bloque les raccourcis système Windows via le registre."""

    # Clé de registre pour les stratégies utilisateur
    REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"

    # Clés à modifier pour bloquer les raccourcis
    REGISTRY_SETTINGS = {
        # Alt+Tab
        "DisableAltTab": 1,
        # Ctrl+Alt+Del
        "DisableCtrlAltDel": 1,
        # Écran de verrouillage par Win+L
        "DisableLockWorkstation": 1,
        # Touche Windows
        "NoWinKeys": 1,
    }

    def __init__(self):
        self.original_values = {}
        self._is_enabled = False

    @staticmethod
    def _is_admin() -> bool:
        """Vérifie si l'application s'exécute avec les droits administrateur."""
        # noinspection broad-exception
        try:
            import ctypes
            # noinspection unresolved-references
            return ctypes.windll.shell.IsUserAnAdmin() != 0
        except Exception:
            return False

    def _get_registry_key(self) -> Optional[winreg.HKEYType]:
        """Ouvre la clé de registre pour modification."""
        try:
            return winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.REGISTRY_PATH,
                0,
                winreg.KEY_WRITE | winreg.KEY_READ,
            )
        except FileNotFoundError:
            # La clé n'existe pas, il faut la créer
            try:
                return winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.REGISTRY_PATH)
            except Exception as e:
                print(f"Erreur lors de la création de la clé de registre : {e}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"Erreur lors de l'accès au registre : {e}", file=sys.stderr)
            return None

    def enable(self) -> bool:
        """Active le blocage des raccourcis système via le registre.

        Retourne True si succès, False sinon.
        """
        if self._is_enabled:
            return True

        if not self._is_admin():
            print("⚠️  Erreur : Les droits administrateur sont nécessaires pour modifier le registre.", file=sys.stderr)
            print("   Lancez l'application en tant qu'administrateur pour utiliser ce module.", file=sys.stderr)
            return False

        key = self._get_registry_key()
        if key is None:
            return False

        try:
            return self._extracted_from_enable_20(key)
        except Exception as e:
            return self._extracted_from_disable_21(
                'Erreur lors du blocage via registre : ', e, key
            )

    # TODO Rename this here and in `enable`
    def _extracted_from_enable_20(self, key):
        # Sauvegarde les valeurs originales
        for setting_name in self.REGISTRY_SETTINGS:
            try:
                value, _ = winreg.QueryValueEx(key, setting_name)
                self.original_values[setting_name] = value
            except FileNotFoundError:
                self.original_values[setting_name] = None

        # Applique les nouveaux paramètres
        for setting_name, setting_value in self.REGISTRY_SETTINGS.items():
            winreg.SetValueEx(key, setting_name, 0, winreg.REG_DWORD, setting_value)

        winreg.CloseKey(key)
        self._is_enabled = True
        print("✓ Raccourcis système bloqués via registre Windows")
        return True

    def disable(self) -> bool:
        """Désactive le blocage et restaure les paramètres originaux.

        Retourne True si succès, False sinon.
        """
        if not self._is_enabled:
            return True

        key = self._get_registry_key()
        if key is None:
            return False

        try:
            return self._extracted_from_disable_15(key)
        except Exception as e:
            return self._extracted_from_disable_21(
                'Erreur lors de la restauration des paramètres : ', e, key
            )

    # TODO Rename this here and in `enable` and `disable`
    @staticmethod
    def _extracted_from_disable_21(arg0, e, key):
        print(f"{arg0}{e}", file=sys.stderr)
        with contextlib.suppress(Exception):
            winreg.CloseKey(key)
        return False

    # TODO Rename this here and in `disable`
    def _extracted_from_disable_15(self, key):
            # Restaure les valeurs originales
        for setting_name, original_value in self.original_values.items():
            if original_value is None:
                    # La clé n'existait pas, on la supprime
                with contextlib.suppress(FileNotFoundError):
                    winreg.DeleteValue(key, setting_name)
            else:
                # Restaure la valeur originale
                winreg.SetValueEx(key, setting_name, 0, winreg.REG_DWORD, original_value)

        winreg.CloseKey(key)
        self._is_enabled = False
        self.original_values.clear()
        print("✓ Raccourcis système restaurés")
        return True

    def is_enabled(self) -> bool:
        """Retourne True si le blocage est actuellement activé."""
        return self._is_enabled


# Singleton global
_registry_blocker: Optional[WindowsRegistryBlocker] = None


def get_registry_blocker() -> WindowsRegistryBlocker:
    """Obtient l'instance globale du bloqueur de registre."""
    global _registry_blocker
    if _registry_blocker is None:
        _registry_blocker = WindowsRegistryBlocker()
    return cast(WindowsRegistryBlocker, _registry_blocker)


def enable_registry_blocking() -> bool:
    """Active le blocage au niveau du registre."""
    return get_registry_blocker().enable()


def disable_registry_blocking() -> bool:
    """Désactive le blocage au niveau du registre."""
    return get_registry_blocker().disable()
