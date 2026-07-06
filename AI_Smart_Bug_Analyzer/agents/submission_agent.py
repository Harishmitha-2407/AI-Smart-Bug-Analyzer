"""
agents/submission_agent.py
--------------------------
TASK 3 – Agent 1: SubmissionAgent  (fully implemented, Phase 1)

Responsibilities
----------------
- Accept a free-text bug description from the UI.
- Accept an uploaded log file (raw bytes + filename).
- Validate both inputs via the Validator utility.
- Merge description and log content into a single structured BugReport.
- Persist the uploaded file to disk.
- Append the report to bug_dataset.csv.
- Return a BugReport dataclass to the caller.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from utils.logger import get_logger
from utils.validator import Validator, ValidationError
from utils.file_handler import FileHandler

logger = get_logger(__name__)


# ── Return type ────────────────────────────────────────────────────────────────

@dataclass
class BugReport:
    """
    Structured representation of a submitted bug.

    Attributes
    ----------
    bug_id      : Auto-generated UUID4 string.
    title       : Short one-line title (first 80 chars of description).
    description : Cleaned free-text description entered by the user.
    log_text    : Decoded content of the uploaded log file (empty if none).
    submitted_at: ISO-8601 UTC timestamp of submission.
    log_filename: Original filename of the upload, or None.
    log_file_path: Absolute path where the upload was saved, or None.
    source      : "text" | "file" | "merged"
    """
    bug_id:        str
    title:         str
    description:   str
    log_text:      str
    submitted_at:  str
    log_filename:  Optional[str]  = None
    log_file_path: Optional[Path] = None
    source:        str            = "text"
    extra:         dict           = field(default_factory=dict)

    def combined_text(self) -> str:
        """Full text for downstream processing (description + log merged)."""
        parts = [p for p in (self.description, self.log_text) if p.strip()]
        return "\n\n--- LOG ---\n\n".join(parts)

    def as_csv_row(self) -> dict:
        """Map to the canonical CSV columns defined in config.BUG_CSV_COLUMNS."""
        return {
            "BugID":               self.bug_id,
            "Title":               self.title,
            "Description":         self.description,
            "Module":              self.extra.get("module", ""),
            "Priority":            self.extra.get("priority", ""),
            "Severity":            self.extra.get("severity", ""),
            "ProgrammingLanguage": self.extra.get("language", ""),
            "OperatingSystem":     self.extra.get("os", ""),
            "StackTrace":          self.log_text,
            "ExpectedBehavior":    self.extra.get("expected", ""),
            "ActualBehavior":      self.extra.get("actual", ""),
            "FixStatus":           "Open",
            "SubmittedAt":         self.submitted_at,
            "LogFileName":         self.log_filename or "",
        }


# ── Agent ──────────────────────────────────────────────────────────────────────

class SubmissionAgent:
    """
    Entry point for all bug report inputs.

    Usage
    -----
    ::

        agent = SubmissionAgent()
        report = agent.submit(
            description="NullPointerException in UserService at line 42",
            log_bytes=uploaded_file_bytes,
            filename="app.log",
        )
    """

    def __init__(self) -> None:
        self._validator    = Validator()
        self._file_handler = FileHandler()
        logger.info("SubmissionAgent initialised.")

    # ── Public API ─────────────────────────────────────────────────────────────

    def submit(
        self,
        description: Optional[str]  = None,
        log_bytes:   Optional[bytes] = None,
        filename:    Optional[str]   = None,
        extra:       Optional[dict]  = None,
    ) -> BugReport:
        """
        Validate, merge, persist, and return a :class:`BugReport`.

        Parameters
        ----------
        description : Free-text bug description from the UI text area.
        log_bytes   : Raw bytes of the uploaded log file.
        filename    : Original filename of the upload.
        extra       : Optional dict for additional metadata
                      (module, priority, severity, language, os, etc.)

        Returns
        -------
        BugReport

        Raises
        ------
        ValidationError subclasses for invalid input.
        """
        try:
            # 1. Validate description
            clean_desc = self._validator.validate_description(description)

            # 2. Validate and decode log file
            clean_log      = ""
            saved_path: Optional[Path] = None

            if log_bytes and filename:
                self._validator.validate_file(filename, len(log_bytes))
                saved_path = self._file_handler.save_upload(filename, log_bytes)
                clean_log  = self._file_handler.read_upload(saved_path)
                logger.info("Log file decoded (%d chars).", len(clean_log))

            # 3. Ensure at least one input is present
            self._validator.validate_submission(clean_desc, bool(log_bytes))

            # 4. Build report
            source = self._determine_source(clean_desc, clean_log)
            report = BugReport(
                bug_id        = f"BUG-{uuid.uuid4().hex[:8].upper()}",
                title         = self._make_title(clean_desc, filename),
                description   = clean_desc,
                log_text      = clean_log,
                submitted_at  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                log_filename  = filename,
                log_file_path = saved_path,
                source        = source,
                extra         = extra or {},
            )

            # 5. Persist to CSV
            self._file_handler.append_to_csv(report.as_csv_row())

            logger.info(
                "BugReport created | id=%s source=%s desc=%d chars log=%d chars",
                report.bug_id, report.source,
                len(report.description), len(report.log_text),
            )
            return report

        except ValidationError:
            raise  # let the UI layer handle these with user-friendly messages
        except Exception as exc:
            logger.exception("Unexpected error in SubmissionAgent.submit: %s", exc)
            raise RuntimeError(f"Submission failed unexpectedly: {exc}") from exc

    # ── Private helpers ────────────────────────────────────────────────────────

    @staticmethod
    def _determine_source(description: str, log_text: str) -> str:
        if description and log_text:
            return "merged"
        if log_text:
            return "file"
        return "text"

    @staticmethod
    def _make_title(description: str, filename: Optional[str]) -> str:
        if description:
            first_line = description.strip().splitlines()[0]
            return first_line[:80]
        if filename:
            return f"Log upload: {filename}"
        return "Untitled bug report"
