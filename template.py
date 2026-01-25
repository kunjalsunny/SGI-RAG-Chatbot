import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

project_root = Path(".")

list_of_dirs = [
    "backend/app",
    "backend/app/api",
    "backend/app/api/routes",
    "backend/app/core",
    "backend/app/rag",
    "docker",
]

list_of_files = [
    "backend/__init__.py",
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/api/__init__.py",
    "backend/app/api/routes/__init__.py",
    "backend/app/api/routes/health.py",
    "backend/app/api/routes/chat.py",
    "backend/app/core/__init__.py",
    "backend/app/core/settings.py",
    "backend/app/rag/__init__.py",
    "backend/app/rag/kb_client.py",
    "requirements.txt",
    ".env",
    ".gitignore",
    "Dockerfile",
    "docker/docker-compose.yml",
    "README.md",
]

for d in list_of_dirs:
    p = project_root / d
    p.mkdir(parents=True, exist_ok=True)
    logging.info(f"Created directory: {p}")

for f in list_of_files:
    p = project_root / f
    p.parent.mkdir(parents=True, exist_ok=True)
    if (not p.exists()) or p.stat().st_size == 0:
        p.write_text("", encoding="utf-8")
        logging.info(f"Created empty file: {p}")
    else:
        logging.info(f"File exists: {p} (skipped)")
