import atexit
import ctypes
import threading
from contextlib import contextmanager, suppress
from typing import Optional, cast

# Constantes API Windows
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105

# Codes de touches virtuelles
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_TAB = 0x09
VK_F4 = 0x73
VK_DELETE = 0x46
VK_ESCAPE = 0x1B
VK_F11 = 0x7A
VK_LALT = 0xA4
VK_RALT = 0xA5
VK_LCTRL = 0xA2
VK_RCTRL = 0xA3


class KBDLLHOOKSTRUCT(ctypes.Structure):
    """Structure pour les événements de clavier low-level."""
    _fields_ = [
        ("vkCode", ctypes.c_uint32),
        ("scanCode", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("time", ctypes.c_uint32),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_void_p)),
    ]

class KeyboardBlocker:
    """Gère le verrouillage du clavier et des raccourcis système Windows via hook global."""

    def __init__(self):
        self.is_locked = False
        self.hook_handle: Optional[int] = None
        self._lock = threading.Lock()
        self.pressed_keys = set()

        # Enregistre le déverrouillage à la fermeture
        atexit.register(self.unlock)

        # Crée la callback (doit être gardée en référence)
        self._hook_callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.POINTER(KBDLLHOOKSTRUCT))(self._keyboard_hook)  # type: ignore

    def _keyboard_hook(
        self,
        nCode: int,
        wParam: int,
        lParam: ctypes._Pointer[KBDLLHOOKSTRUCT]
    ) -> int:
        """Callback pour le hook clavier global."""
        if not self.is_locked or nCode != 0:
            # Passe l'événement au hook suivant
            # noinspection unresolved-references
            return ctypes.windll.user32.CallNextHookEx(
                self.hook_handle, nCode, wParam, lParam
            )

        if not lParam:
            # noinspection unresolved-references
            return ctypes.windll.user32.CallNextHookEx(
                self.hook_handle, nCode, wParam, lParam
            )

        # noinspection broad-exception
        with suppress(Exception):
            kb = lParam.contents
            vk_code = kb.vkCode
            is_pressed = wParam in (WM_KEYDOWN, WM_SYSKEYDOWN)
            is_released = wParam in (WM_KEYUP, WM_SYSKEYUP)

            with self._lock:
                # Enregistre les touches pressées
                if is_pressed:
                    self.pressed_keys.add(vk_code)
                elif is_released:
                    self.pressed_keys.discard(vk_code)

                # Vérifie si c'est un raccourci à bloquer
                if self._should_block_key(vk_code):
                    return 1  # Bloque l'événement (1 = événement consommé)

        # Passe l'événement au hook suivant
        # noinspection unresolved-references
        return ctypes.windll.user32.CallNextHookEx(
            self.hook_handle, nCode, wParam, lParam
        )
    def _should_block_key(self, vk_code: int) -> bool:
        """Détermine si une touche doit être bloquée."""
        # Bloquer les touches Windows
        if vk_code in (VK_LWIN, VK_RWIN):
            return True

        # Bloquer Alt+Tab
        if vk_code == VK_TAB and self._is_alt_pressed():
            return True

        # Bloquer Alt+F4
        if vk_code == VK_F4 and self._is_alt_pressed():
            return True

        # Bloquer Ctrl+Alt+Del
        if (vk_code == VK_DELETE and
                self._is_alt_pressed() and
                self._is_ctrl_pressed()):
            return True

        return vk_code in [VK_F11, VK_ESCAPE]

    def _is_alt_pressed(self) -> bool:
        """Vérifie si Alt est pressé."""
        return VK_LALT in self.pressed_keys or VK_RALT in self.pressed_keys

    def _is_ctrl_pressed(self) -> bool:
        """Vérifie si Ctrl est pressé."""
        return VK_LCTRL in self.pressed_keys or VK_RCTRL in self.pressed_keys

    def lock(self) -> bool:
        """Verrouille le clavier et les raccourcis système.

        Retourne True si succès, False sinon.
        """
        if self.is_locked:
            return True

        # noinspection broad-exception
        try:
            # Installe le hook global de clavier
            # noinspection unresolved-references
            self.hook_handle = ctypes.windll.user32.SetWindowsHookExW(
                WH_KEYBOARD_LL,
                self._hook_callback,
                None,
                0
            )

            if self.hook_handle is None or self.hook_handle == 0:
                return False

            self.is_locked = True
            return True

        except Exception:
            return False

    def unlock(self) -> bool:
        """Déverrouille le clavier et les raccourcis système.

        Retourne True si succès, False sinon.
        """
        if not self.is_locked:
            return True

        # noinspection broad-exception
        try:
            if self.hook_handle is not None and self.hook_handle != 0:
                # noinspection unresolved-references
                result = ctypes.windll.user32.UnhookWindowsHookEx(self.hook_handle)
                self.hook_handle = None
                self.is_locked = False
                self.pressed_keys.clear()
                return result != 0

            return True

        except Exception:
            return False

    @contextmanager
    def locked(self):
        """Context manager pour verrouiller/déverrouiller le clavier."""
        self.lock()
        try:
            yield
        finally:
            self.unlock()


# Instance globale
_keyboard_blocker: Optional[KeyboardBlocker] = None


def get_keyboard_blocker() -> KeyboardBlocker:
    """Obtient l'instance globale du verrouilleur de clavier."""
    global _keyboard_blocker
    if _keyboard_blocker is None:
        _keyboard_blocker = KeyboardBlocker()
    return cast(KeyboardBlocker, _keyboard_blocker)


def lock_keyboard() -> bool:
    """Verrouille le clavier."""
    return get_keyboard_blocker().lock()


def unlock_keyboard() -> bool:
    """Déverrouille le clavier."""
    return get_keyboard_blocker().unlock()
