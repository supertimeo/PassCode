"""
Watcher de session Windows : lance PassCode à chaque déverrouillage de session.

Contrairement au Task Scheduler (trigger "SessionUnlock"), qui dépend d'un token
de session interactive pouvant expirer silencieusement (déconnexion, veille,
redémarrage du service Task Scheduler...), ce watcher écoute directement les
messages système WM_WTSSESSION_CHANGE envoyés par Windows à toute fenêtre
enregistrée via WTSRegisterSessionNotification. C'est le mécanisme natif utilisé
par les écrans de veille et logiciels de session d'entreprise : il ne dépend
d'aucun service tiers et reste fiable indéfiniment tant que ce processus tourne.

Utilise une vraie fenêtre top-level cachée (jamais affichée), pas une fenêtre
"message-only" (HWND_MESSAGE) : cette dernière n'est pas garantie de recevoir
les notifications de session de façon fiable sur tous les cycles verrouillage/
déverrouillage (comportement documenté, contrairement aux exemples officiels
Microsoft qui utilisent tous une fenêtre cachée classique).

Ce script tourne en arrière-plan (lancé au démarrage via le registre Run) et
lance PassCode.exe à chaque événement de déverrouillage.

Quand l'option "au déverrouillage" est choisie, l'installateur inscrit à la
fois PassCode.exe (pour le tout premier démarrage/ouverture de session) et ce
watcher (pour les déverrouillages suivants) dans le registre Run — les deux se
lancent donc en même temps au login. Or Windows envoie parfois, juste après le
login, un faux événement WTS_SESSION_UNLOCK (artefact du fast startup/hybrid
boot). Pour éviter que le watcher ne lance un second PassCode.exe en doublon
dans ce cas, il ignore tout événement reçu pendant les STARTUP_GRACE_SECONDS
premières secondes après son propre démarrage.
"""

import ctypes
import ctypes.wintypes as wintypes
import subprocess
import sys
import time
import traceback
from pathlib import Path

WM_WTSSESSION_CHANGE = 0x02B1
WTS_SESSION_UNLOCK = 0x8
NOTIFY_FOR_THIS_SESSION = 0
WM_DESTROY = 0x0002
ERROR_ALREADY_EXISTS = 183
STARTUP_GRACE_SECONDS = 20

WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)


class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HANDLE),
        ("hIcon", wintypes.HANDLE),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HANDLE),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


def _get_exe_path() -> str:
    """Chemin de PassCode.exe, à côté du watcher."""
    return str(Path(sys.executable).resolve().parent / "PassCode.exe")


def _log_error(context: str) -> None:
    log_path = Path(sys.executable).resolve().parent / "PassCode_Watcher_error.log"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"--- {context} ---\n")
        f.write(traceback.format_exc())
        f.write("\n")


def _launch_passcode() -> None:
    try:
        subprocess.Popen([_get_exe_path()])
    except Exception:
        _log_error("Echec du lancement de PassCode.exe")


_startup_time = time.monotonic()


def _within_startup_grace_period() -> bool:
    return (time.monotonic() - _startup_time) < STARTUP_GRACE_SECONDS


def _window_proc(hwnd, msg, wparam, lparam):
    if msg == WM_WTSSESSION_CHANGE and wparam == WTS_SESSION_UNLOCK:
        if not _within_startup_grace_period():
            _launch_passcode()
    elif msg == WM_DESTROY:
        ctypes.windll.user32.PostQuitMessage(0)
    return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)


def _acquire_single_instance_lock() -> bool:
    """Empêche deux watchers de tourner en même temps."""
    handle = ctypes.windll.kernel32.CreateMutexW(None, False, "PassCodeSessionWatcherMutex")
    if not handle:
        return True  # échec de création du mutex : on continue quand même
    return ctypes.windll.kernel32.GetLastError() != ERROR_ALREADY_EXISTS


def main() -> None:
    if not _acquire_single_instance_lock():
        return

    user32 = ctypes.windll.user32
    wtsapi32 = ctypes.windll.wtsapi32

    wndproc = WNDPROC(_window_proc)
    hinstance = ctypes.windll.kernel32.GetModuleHandleW(None)
    class_name = "PassCodeSessionWatcher"

    wndclass = WNDCLASS()
    wndclass.style = 0
    wndclass.lpfnWndProc = wndproc
    wndclass.cbClsExtra = 0
    wndclass.cbWndExtra = 0
    wndclass.hInstance = hinstance
    wndclass.hIcon = None
    wndclass.hCursor = None
    wndclass.hbrBackground = None
    wndclass.lpszMenuName = None
    wndclass.lpszClassName = class_name

    user32.RegisterClassW(ctypes.byref(wndclass))

    # Fenêtre top-level classique, jamais affichée (pas de WS_VISIBLE) :
    # contrairement à une fenêtre "message-only" (HWND_MESSAGE), c'est le type
    # de fenêtre utilisé par tous les exemples officiels Microsoft pour
    # recevoir WM_WTSSESSION_CHANGE de façon fiable sur la durée.
    hwnd = user32.CreateWindowExW(
        0, class_name, "PassCodeSessionWatcher", 0,
        0, 0, 0, 0,
        None, None, hinstance, None,
    )

    if not hwnd:
        _log_error("CreateWindowExW a échoué")
        return

    if not wtsapi32.WTSRegisterSessionNotification(hwnd, NOTIFY_FOR_THIS_SESSION):
        _log_error("WTSRegisterSessionNotification a échoué")
        return

    try:
        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
    except Exception:
        _log_error("Erreur dans la boucle de messages")
    finally:
        wtsapi32.WTSUnRegisterSessionNotification(hwnd)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        _log_error("Erreur fatale dans main()")
