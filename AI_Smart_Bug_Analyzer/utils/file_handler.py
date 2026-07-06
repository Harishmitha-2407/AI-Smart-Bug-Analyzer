"""
utils/file_handler.py
---------------------
Handles persisting uploaded log files and appending rows to bug_dataset.csv.
"""

import csv
import os
from pathlib import Path
from typing import Any

import config
from utils.logger import get_logger

logger = get_logger(__name__)


class FileHandler:
    """Manages all file I/O for the bug submission pipeline."""

    # ── Upload persistence ─────────────────────────────────────────────────────

    def save_upload(self, filename: str, content: bytes) -> Path:
        """
        Persist raw upload bytes to ``data/uploaded_logs/``.

        Parameters
        ----------
        filename : Original filename from the uploader widget.
        content  : Raw bytes of the uploaded file.

        Returns
        -------
        Path
            Absolute path of the saved file.
        """
        config.UPLOADED_LOGS_DIR.mkdir(parents=True, exist_ok=True)
        dest = config.UPLOADED_LOGS_DIR / filename

        with open(dest, "wb") as fh:
            fh.write(content)

        logger.info("Upload saved → %s (%d bytes)", dest, len(content))
        return dest

    def read_upload(self, path: Path) -> str:
        """Decode a saved upload and return its text content."""
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()

    # ── CSV persistence ────────────────────────────────────────────────────────

    def append_to_csv(self, row: dict[str, Any]) -> None:
        """
        Append *row* to ``bug_dataset.csv``.
        Creates the file with a header row if it does not yet exist.

        Parameters
        ----------
        row : Dict whose keys must be a subset of ``config.BUG_CSV_COLUMNS``.
        """
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        path       = config.BUG_DATASET_PATH
        write_header = not path.exists() or path.stat().st_size == 0

        with open(path, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=config.BUG_CSV_COLUMNS,
                extrasaction="ignore",
            )
            if write_header:
                writer.writeheader()
            writer.writerow(row)

        logger.info("Bug appended to CSV → %s", path)

    def ensure_csv_exists(self) -> None:
        """Create ``bug_dataset.csv`` with headers if it does not exist."""
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = config.BUG_DATASET_PATH
        if not path.exists() or path.stat().st_size == 0:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=config.BUG_CSV_COLUMNS)
                writer.writeheader()
            logger.info("Created empty bug_dataset.csv at %s", path)
