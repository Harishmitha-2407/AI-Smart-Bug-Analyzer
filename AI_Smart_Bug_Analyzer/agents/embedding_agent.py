"""
agents/embedding_agent.py
--------------------------
TASK 3 – Agent 3: EmbeddingAgent  (PLACEHOLDER – Phase 2)

This agent will convert cleaned bug-report text into dense vector
embeddings using a SentenceTransformer model.  No embedding logic is
implemented in Phase 1.

Future responsibilities (Phase 2)
----------------------------------
- Load a pre-trained SentenceTransformer model (e.g. all-MiniLM-L6-v2).
- Encode a list of text chunks into float vectors.
- Encode a single query string for similarity search.
- Cache the model so it is loaded only once per session.

Why embeddings?
---------------
Text embeddings map semantically similar sentences close together in
high-dimensional vector space.  This lets us find bugs that are
*conceptually* similar even when the exact wording differs — something
keyword search cannot do.
"""

from typing import Any
from utils.logger import get_logger

logger = get_logger(__name__)

_PLACEHOLDER_MSG = (
    "EmbeddingAgent is a Phase 2 feature. "
    "Embedding generation is not yet implemented."
)


class EmbeddingAgent:
    """
    [PLACEHOLDER] Converts text into vector embeddings.

    All public methods raise :class:`NotImplementedError` and log a
    clear message so callers receive a helpful error instead of a
    cryptic failure.

    Phase 2 implementation will require:
        pip install sentence-transformers torch
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        """
        Parameters
        ----------
        model_name : HuggingFace model identifier (Phase 2 only).
        """
        self.model_name = model_name
        logger.warning("EmbeddingAgent instantiated in PLACEHOLDER mode.")

    # ── Stub methods ───────────────────────────────────────────────────────────

    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        [Phase 2] Encode a list of strings into embedding vectors.

        Parameters
        ----------
        texts : Non-empty list of cleaned text strings.

        Returns
        -------
        list[list[float]]
            One float vector per input string.
        """
        logger.error(_PLACEHOLDER_MSG)
        raise NotImplementedError(_PLACEHOLDER_MSG)

    def embed_query(self, query: str) -> list[float]:
        """
        [Phase 2] Encode a single query string.

        Parameters
        ----------
        query : User bug description or search query.

        Returns
        -------
        list[float]  Embedding vector.
        """
        logger.error(_PLACEHOLDER_MSG)
        raise NotImplementedError(_PLACEHOLDER_MSG)

    def get_model_info(self) -> dict[str, Any]:
        """Return metadata about the configured model (stub)."""
        return {
            "model_name":  self.model_name,
            "status":      "not_loaded",
            "phase":       2,
            "description": "Sentence-Transformers embedding model",
        }
