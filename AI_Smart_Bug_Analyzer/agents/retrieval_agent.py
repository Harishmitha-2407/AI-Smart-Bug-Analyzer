"""
agents/retrieval_agent.py
--------------------------
TASK 3 – Agent 4: RetrievalAgent  (PLACEHOLDER – Phase 2)

This agent will query a ChromaDB vector database with an embedding
vector and return the most semantically similar stored bug reports.
No vector-database connection is implemented in Phase 1.

Future responsibilities (Phase 2)
----------------------------------
- Accept a query embedding (list[float]) from EmbeddingAgent.
- Connect to a local ChromaDB persistent store.
- Run a cosine-similarity nearest-neighbour query.
- Return the top-K most similar bug documents with their metadata.

Why vector similarity search?
------------------------------
Traditional SQL "LIKE" queries match exact substrings.  Vector search
finds documents that are *semantically* close — e.g. "server keeps
crashing" matches "application unexpectedly terminates" — enabling
far more useful bug retrieval.
"""

from typing import Any
from utils.logger import get_logger

logger = get_logger(__name__)

_PLACEHOLDER_MSG = (
    "RetrievalAgent is a Phase 2 feature. "
    "Vector database connection is not yet implemented."
)


class RetrievalAgent:
    """
    [PLACEHOLDER] Retrieves similar bugs from the vector database.

    Phase 2 implementation will require:
        pip install chromadb
    """

    def __init__(self, db_path: str = "./chroma_store") -> None:
        """
        Parameters
        ----------
        db_path : Path to the ChromaDB persistent store (Phase 2 only).
        """
        self.db_path = db_path
        logger.warning("RetrievalAgent instantiated in PLACEHOLDER mode.")

    # ── Stub methods ───────────────────────────────────────────────────────────

    def retrieve(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        [Phase 2] Return the top-K most similar bugs.

        Parameters
        ----------
        query_embedding : Dense vector from EmbeddingAgent.embed_query().
        top_k           : Number of results to return.

        Returns
        -------
        list[dict]
            Each dict has keys: bug_id, document, metadata, similarity.
        """
        logger.error(_PLACEHOLDER_MSG)
        raise NotImplementedError(_PLACEHOLDER_MSG)

    def store_document(
        self,
        bug_id:    str,
        embedding: list[float],
        document:  str,
        metadata:  dict[str, Any],
    ) -> None:
        """
        [Phase 2] Upsert a bug document into ChromaDB.

        Parameters
        ----------
        bug_id    : Unique identifier.
        embedding : Pre-computed embedding vector.
        document  : Text chunk to store.
        metadata  : Associated metadata dict.
        """
        logger.error(_PLACEHOLDER_MSG)
        raise NotImplementedError(_PLACEHOLDER_MSG)

    def get_collection_info(self) -> dict[str, Any]:
        """Return metadata about the vector store (stub)."""
        return {
            "db_path":   self.db_path,
            "status":    "not_connected",
            "phase":     2,
            "backend":   "ChromaDB (planned)",
        }
