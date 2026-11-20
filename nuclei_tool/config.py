import os
import platform
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Directory where config.py is located (nuclei_tool folder)
TOOL_DIR = Path(__file__).resolve().parent

# Default path: bin folder next to config.py
BIN_DIR = TOOL_DIR / "bin"
BINARY_NAME = "nuclei.exe" if platform.system() == "Windows" else "nuclei"
DEFAULT_NUCLEI = BIN_DIR / BINARY_NAME
DEFAULT_TEMPLATES = BIN_DIR / "nuclei-templates"

def _resolve_nuclei() -> str:
    # 1. Check .env
    env_path = os.getenv("NUCLEI_PATH")
    if env_path and Path(env_path).is_file():
        return env_path

    # 2. Check system default location (Windows)
    if platform.system() == "Windows":
        local = Path(r"C:\Tools\nuclei\nuclei.exe")
        if local.is_file():
            return str(local)

    # 3. Check project bin folder
    if DEFAULT_NUCLEI.is_file():
        return str(DEFAULT_NUCLEI)

    # 4. Fallback to system PATH
    return "nuclei"

def _resolve_templates() -> str:
    env_tpl = os.getenv("NUCLEI_TEMPLATES")
    if env_tpl and Path(env_tpl).is_dir():
        return env_tpl

    if platform.system() == "Windows":
        default = Path.home() / "nuclei-templates"
        if default.is_dir():
            return str(default)

    if DEFAULT_TEMPLATES.is_dir():
        return str(DEFAULT_TEMPLATES)

    return ""

NUCLEI_PATH = _resolve_nuclei()
NUCLEI_TEMPLATES = _resolve_templates()

print(f"[config] nuclei  -> {NUCLEI_PATH}")
print(f"[config] templates -> {NUCLEI_TEMPLATES or '(default)'}")