import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
EVIDENCE_DIR = UPLOAD_DIR / "evidence"
REPORTS_DIR = BASE_DIR.parent / "reports"
DEMO_ASSETS_DIR = BASE_DIR / "demo_assets"

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
DEMO_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "legal-metrology-sih26034-officer-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Database
DATABASE_URL = f"sqlite:///{BASE_DIR}/legal_metrology.db"
