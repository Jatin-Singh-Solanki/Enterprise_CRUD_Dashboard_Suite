from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
APP_DIR = BASE_DIR / "app"
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "atlasnexus_prosuite.db"
STATIC_DIR = APP_DIR / "static"
TEMPLATE_DIR = APP_DIR / "templates"
APP_NAME = "AtlasNexus ProSuite"
APP_VERSION = "2.0.0"
HOST = "127.0.0.1"
PORT = 8000
