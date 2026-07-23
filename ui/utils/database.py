from pathlib import Path

from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "trend_detection.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)