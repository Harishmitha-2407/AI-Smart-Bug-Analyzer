"""
utils/cleaner.py
----------------
Text-cleaning helpers used by PreprocessingAgent.

Cleaning steps (applied in order):
    1. Lowercase
    2. Strip HTML tags
    3. Remove URLs
    4. Remove punctuation
    5. Remove special / non-ASCII characters
    6. Collapse extra whitespace
"""

import re
import html
from utils.logger import get_logger

logger = get_logger(__name__)

# Pre-compiled patterns for performance
_HTML_TAG    = re.compile(r"<[^>]+>")
_URL         = re.compile(r"https?://\S+|www\.\S+")
_PUNCTUATION = re.compile(r"[^\w\s]")          # keep word-chars and spaces
_NON_ASCII   = re.compile(r"[^\x00-\x7F]+")
_MULTI_SPACE = re.compile(r"\s+")


class Cleaner:
    """Stateless text-cleaning utility."""

    # ── Public API ─────────────────────────────────────────────────────────────

    def clean(self, text: str) -> str:
        """
        Apply the full cleaning pipeline to *text*.

        Parameters
        ----------
        text : Raw input string.

        Returns
        -------
        str
            Cleaned, normalised string.
        """
        if not isinstance(text, str):
            logger.warning("clean() received %s; converting to str.", type(text).__name__)
            text = str(text)

        text = self._decode_html_entities(text)
        text = self._to_lowercase(text)
        text = self._strip_html_tags(text)
        text = self._remove_urls(text)
        text = self._remove_punctuation(text)
        text = self._remove_non_ascii(text)
        text = self._collapse_whitespace(text)

        logger.debug("Cleaned text (first 80 chars): %r", text[:80])
        return text

    def clean_log(self, text: str) -> str:
        """
        Lighter cleaning for log files — preserves structure (newlines, colons)
        but removes ANSI escape codes and normalises whitespace.
        """
        _ANSI = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
        text  = _ANSI.sub("", text)
        text  = self._decode_html_entities(text)
        text  = self._to_lowercase(text)
        text  = self._remove_non_ascii(text)
        text  = re.sub(r"[ \t]{2,}", " ", text)   # collapse horizontal space only
        text  = re.sub(r"\n{3,}", "\n\n", text)   # max two consecutive newlines
        return text.strip()

    # ── Private steps ──────────────────────────────────────────────────────────

    @staticmethod
    def _decode_html_entities(text: str) -> str:
        return html.unescape(text)

    @staticmethod
    def _to_lowercase(text: str) -> str:
        return text.lower()

    @staticmethod
    def _strip_html_tags(text: str) -> str:
        return _HTML_TAG.sub(" ", text)

    @staticmethod
    def _remove_urls(text: str) -> str:
        return _URL.sub(" ", text)

    @staticmethod
    def _remove_punctuation(text: str) -> str:
        return _PUNCTUATION.sub(" ", text)

    @staticmethod
    def _remove_non_ascii(text: str) -> str:
        return _NON_ASCII.sub(" ", text)

    @staticmethod
    def _collapse_whitespace(text: str) -> str:
        return _MULTI_SPACE.sub(" ", text).strip()
