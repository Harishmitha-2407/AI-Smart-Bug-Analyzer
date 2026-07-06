"""
utils/validator.py
------------------
Input validation helpers for the Bug Submission Module.

Raises typed exceptions so callers can display precise error messages.
"""

import os
from utils.logger import get_logger
import config

logger = get_logger(__name__)

ALLOWED_EXTENSIONS: frozenset[str] = frozenset({".txt", ".log"})


# ── Custom exceptions ──────────────────────────────────────────────────────────

class ValidationError(ValueError):
    """Base class for all submission validation errors."""


class EmptyInputError(ValidationError):
    """Both description and log file are empty."""


class DescriptionTooLongError(ValidationError):
    """Bug description exceeds the character limit."""


class InvalidFileTypeError(ValidationError):
    """Uploaded file has an unsupported extension."""


class FileTooLargeError(ValidationError):
    """Uploaded file exceeds the byte-size limit."""


# ── Validator ─────────────────────────────────────────────────────────────────

class Validator:
    """
    Validates submission inputs before they reach the agent layer.

    All methods raise a :class:`ValidationError` subclass on failure,
    or return the (possibly trimmed) value on success.
    """

    def validate_description(self, text: str | None) -> str:
        """
        Validate and return the cleaned description string.

        Raises
        ------
        DescriptionTooLongError
        """
        text = (text or "").strip()

        if len(text) > config.MAX_DESCRIPTION_CHARS:
            raise DescriptionTooLongError(
                f"Description is {len(text):,} characters. "
                f"Maximum allowed is {config.MAX_DESCRIPTION_CHARS:,}."
            )

        logger.debug("Description valid (%d chars).", len(text))
        return text

    def validate_file(self, filename: str, size_bytes: int) -> None:
        """
        Check file extension and size.

        Raises
        ------
        InvalidFileTypeError
        FileTooLargeError
        """
        ext = os.path.splitext(filename)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise InvalidFileTypeError(
                f"File type '{ext}' is not supported. "
                f"Please upload a {' or '.join(ALLOWED_EXTENSIONS)} file."
            )

        if size_bytes > config.MAX_LOG_FILE_BYTES:
            kb = config.MAX_LOG_FILE_BYTES // 1024
            raise FileTooLargeError(
                f"File is {size_bytes / 1024:.1f} KB. "
                f"Maximum allowed size is {kb} KB."
            )

        logger.debug("File '%s' passed validation (%d bytes).", filename, size_bytes)

    def validate_submission(self, description: str, has_file: bool) -> None:
        """
        Ensure at least one input is provided.

        Raises
        ------
        EmptyInputError
        """
        if not description and not has_file:
            raise EmptyInputError(
                "Submission is empty. "
                "Please provide a bug description, upload a log file, or both."
            )
