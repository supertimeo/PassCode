"""
Force une fenêtre au premier plan de façon fiable sur Windows.

Windows bloque volontairement les appels "naïfs" à SetForegroundWindow pour
empêcher les applications de voler le focus sans interaction utilisateur
(protection anti-spam appelée "foreground lock"). Un process qui vient d'être
lancé par le watcher de déverrouillage, sans input utilisateur récent, se
heurte exactement à cette restriction : la fenêtre s'affiche mais reste
derrière le bureau ou une autre fenêtre déjà active, ce qui laisse les
raccourcis clavier bloqués mais permet quand même d'interagir avec ce qui est
au premier plan.

La technique fiable pour contourner cette restriction est d'attacher
temporairement la file d'entrée du thread courant à celle du thread
propriétaire de la fenêtre actuellement au premier plan (AttachThreadInput),
ce qui autorise SetForegroundWindow pour la durée de l'attachement.
"""

import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

SW_SHOW = 5
HWND_TOPMOST = -1


def force_window_foreground(hwnd: int) -> None:
    """Force la fenêtre `hwnd` au premier plan et lui donne le focus."""
    foreground_hwnd = user32.GetForegroundWindow()
    foreground_thread = user32.GetWindowThreadProcessId(foreground_hwnd, None)
    current_thread = kernel32.GetCurrentThreadId()

    attached = False
    if foreground_thread and foreground_thread != current_thread:
        attached = bool(user32.AttachThreadInput(current_thread, foreground_thread, True))

    try:
        user32.ShowWindow(hwnd, SW_SHOW)
        user32.SetWindowPos(
            hwnd, HWND_TOPMOST, 0, 0, 0, 0,
            wintypes.UINT(0x0001 | 0x0002),  # SWP_NOSIZE | SWP_NOMOVE
        )
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
    finally:
        if attached:
            user32.AttachThreadInput(current_thread, foreground_thread, False)
