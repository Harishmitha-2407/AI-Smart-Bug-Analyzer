"""
config.py
---------
Central configuration for AI Smart Bug Analyzer (Phase 1 — Tasks 1-5).
All runtime settings live here so no magic strings are scattered across modules.
"""

import os
from pathlib import Path

# ── Project root ───────────────────────────────────────────────────────────────
BASE_DIR: Path = Path(__file__).parent.resolve()

# ── Data paths ─────────────────────────────────────────────────────────────────
DATA_DIR:          Path = BASE_DIR / "data"
UPLOADED_LOGS_DIR: Path = DATA_DIR / "uploaded_logs"
BUG_DATASET_PATH:  Path = DATA_DIR / "bug_dataset.csv"

# ── Logging ────────────────────────────────────────────────────────────────────
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# ── Submission constraints ─────────────────────────────────────────────────────
MAX_DESCRIPTION_CHARS: int = 10_000
MAX_LOG_FILE_BYTES:    int = 512 * 1024   # 512 KB

# ── CSV columns (canonical order) ─────────────────────────────────────────────
BUG_CSV_COLUMNS: list[str] = [
    "BugID", "Title", "Description", "Module", "Priority", "Severity",
    "ProgrammingLanguage", "OperatingSystem", "StackTrace",
    "ExpectedBehavior", "ActualBehavior", "FixStatus",
    "SubmittedAt", "LogFileName",
]

# ── App metadata ───────────────────────────────────────────────────────────────
APP_TITLE:   str = "AI Smart Bug Analyzer & Fix Advisor"
APP_VERSION: str = "1.0.0 (Phase 1)"
APP_ICON:    str = "🐛"
