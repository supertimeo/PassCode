import sys
from pathlib import Path

# Déterminer le chemin racine (fonctionne aussi avec PyInstaller)
if getattr(sys, 'frozen', False):
    # Exécutable PyInstaller
    base_path = Path(sys._MEIPASS)
else:
    # Développement
    base_path = Path(__file__).resolve().parent.parent.parent

log_folder_path = base_path / "logs"
assets_folder_path = base_path / "assets"
configs_folder_path = base_path / "configs"