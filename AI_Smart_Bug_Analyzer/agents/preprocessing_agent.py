"""
agents/preprocessing_agent.py
------------------------------
TASK 3 – Agent 2: PreprocessingAgent  (fully implemented, Phase 1)

Responsibilities
----------------
- Lowercase text
- Remove HTML tags
- Remove URLs
- Remove punctuation
- Remove special / non-ASCII characters
- Collapse extra whitespace
- Clean uploaded log file text (lighter pipeline, preserves structure)
"""

from typing import Any
from utils.cleaner import Cleaner
from utils.logger import get_logger

logger = get_logger(__name__)


class PreprocessingAgent:
    """
    Cleans and normalises text from a submitted bug report.

    The agent exposes two entry points:

    * :meth:`process_description` — full cleaning for the description field.
    * :meth:`process_log`         — lighter cleaning for raw log content.
    * :meth:`process`             — convenience wrapper that returns both.

    Parameters
    ----------
    cleaner : Optional :class:`~utils.cleaner.Cleaner` instance.
              A default instance is created if not supplied.
    """

    def __init__(self, cleaner: Cleaner | None = None) -> None:
        self._cleaner = cleaner or Cleaner()
        logger.info("PreprocessingAgent initialised.")

    # ── Public API ─────────────────────────────────────────────────────────────

    def process_description(self, text: str) -> str:
        """
        Apply the full cleaning pipeline to a bug description.

        Steps: lowercase → strip HTML → remove URLs → remove punctuation
               → remove non-ASCII → collapse whitespace.

        Parameters
        ----------
        text : Raw description string.

        Returns
        -------
        str  Cleaned description.
        """
        if not text or not text.strip():
            logger.debug("process_description received empty input.")
            return ""
        cleaned = self._cleaner.clean(text)
        logger.info("Description cleaned (%d → %d chars).", len(text), len(cleaned))
        return cleaned

    def process_log(self, log_text: str) -> str:
        """
        Apply a lighter cleaning pass to raw log / stack-trace content.
        Preserves newlines and structural characters (colons, brackets).

        Parameters
        ----------
        log_text : Raw log file content.

        Returns
        -------
        str  Cleaned log text.
        """
        if not log_text or not log_text.strip():
            logger.debug("process_log received empty input.")
            return ""
        cleaned = self._cleaner.clean_log(log_text)
        logger.info("Log cleaned (%d → %d chars).", len(log_text), len(cleaned))
        return cleaned

    def process(self, submission: Any) -> dict[str, str]:
        """
        Process a BugReport (or any object with ``.description``
        and ``.log_text`` attributes) and return a dict with
        ``clean_description`` and ``clean_log``.

        Parameters
        ----------
        submission : Object exposing ``.description`` and ``.log_text``.

        Returns
        -------
        dict[str, str]
            Keys: ``"clean_description"``, ``"clean_log"``
        """
        try:
            result = {
                "clean_description": self.process_description(
                    getattr(submission, "description", "")
                ),
                "clean_log": self.process_log(
                    getattr(submission, "log_text", "")
                ),
            }
            logger.info(
                "Preprocessing complete | source=%s",
                getattr(submission, "source", "unknown"),
            )
            return result
        except Exception as exc:
            logger.exception("Preprocessing failed: %s", exc)
            raise
