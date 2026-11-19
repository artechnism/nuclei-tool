import os
import platform
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def _resolve_nuclei() -> str:
    # ۱. اگه توی .env ست شده بود، از همون استفاده کن
    env_path = os.getenv("NUCLEI_PATH")
    if env_path and Path(env_path).is_file():
        return env_path

    # ۲. مسیر سیستم خودت (ویندوز)
    if platform.system() == "Windows":
        local = Path(r"C:\Tools\nuclei\nuclei.exe")
        if local.is_file():
            return str(local)

    # ۳. fallback: داخل پروژه
    bundled = PROJECT_ROOT / "bin" / ("nuclei.exe" if platform.system() == "Windows" else "nuclei")
    if bundled.is_file():
        return str(bundled)

    # ۴. آخرین تلاش: از PATH
    return "nuclei"

def _resolve_templates() -> str:
    env_tpl = os.getenv("NUCLEI_TEMPLATES")
    if env_tpl and Path(env_tpl).is_dir():
        return env_tpl

    # تمپلیت‌های پیش‌فرض Nuclei روی ویندوز
    if platform.system() == "Windows":
        default = Path.home() / "nuclei-templates"
        if default.is_dir():
            return str(default)

    bundled = PROJECT_ROOT / "bin" / "nuclei-templates"
    if bundled.is_dir():
        return str(bundled)

    return ""  # خالی = nuclei خودش پیش‌فرض رو استفاده می‌کنه

NUCLEI_PATH = _resolve_nuclei()
NUCLEI_TEMPLATES = _resolve_templates()

print(f"[config] nuclei  → {NUCLEI_PATH}")
print(f"[config] templates → {NUCLEI_TEMPLATES or '(default)'}")