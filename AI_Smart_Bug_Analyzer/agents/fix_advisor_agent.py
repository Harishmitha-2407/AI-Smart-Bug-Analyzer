"""
agents/fix_advisor_agent.py
----------------------------
TASK 3 – Agent 5: FixAdvisorAgent  (PLACEHOLDER – Phase 2)

This agent will send a bug report and retrieved similar bugs to a
large language model (Google Gemini) and stream back a structured
fix recommendation.  No LLM integration is implemented in Phase 1.

Future responsibilities (Phase 2)
----------------------------------
- Accept a bug report and top-K retrieved similar bugs.
- Build a structured RAG prompt combining context + query.
- Call the Gemini API (or equivalent LLM).
- Parse and return a structured advisory:
    * Root Cause Analysis
    * Severity Assessment
    * Step-by-Step Fix
    * Code Snippet (if applicable)
    * Prevention Tips

Why RAG for fix advice?
------------------------
Retrieval-Augmented Generation grounds the LLM's response in *real*
similar bugs from your own knowledge base, reducing hallucinations and
providing fixes that are relevant to your specific codebase and tech
stack.
"""

from typing import Any
from utils.logger import get_logger

logger = get_logger(__name__)

_PLACEHOLDER_MSG = (
    "FixAdvisorAgent is a Phase 2 feature. "
    "LLM/Gemini integration is not yet implemented."
)

# Placeholder response shown in the UI during Phase 1
PLACEHOLDER_ADVISORY = """
## 🚧 AI Fix Advisory — Coming in Phase 2

The AI-powered fix recommendation engine is not yet active.

**What will be available in Phase 2:**

1. **Root Cause Analysis** — Gemini will analyse your bug description
   and similar historical bugs to identify the likely root cause.

2. **Severity Assessment** — Automatic classification as
   Critical / High / Medium / Low with justification.

3. **Step-by-Step Fix** — Concrete, actionable remediation steps
   tailored to your tech stack.

4. **Code Snippet** — A corrected or illustrative code example
   where applicable.

5. **Prevention Tips** — Patterns and practices to avoid this
   class of bug in future.

---
*Your bug has been successfully submitted and stored.
The AI analysis pipeline will be connected in Phase 2.*
""".strip()


class FixAdvisorAgent:
    """
    [PLACEHOLDER] Generates AI-powered fix recommendations.

    Phase 2 implementation will require:
        pip install google-generativeai
    and a valid GEMINI_API_KEY in .env
    """

    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        """
        Parameters
        ----------
        model_name : Gemini model identifier (Phase 2 only).
        """
        self.model_name = model_name
        logger.warning("FixAdvisorAgent instantiated in PLACEHOLDER mode.")

    # ── Stub methods ───────────────────────────────────────────────────────────

    def advise(
        self,
        bug_report:  str,
        similar_bugs: list[dict[str, Any]],
    ) -> str:
        """
        [Phase 2] Generate a fix advisory using Gemini + RAG context.

        Parameters
        ----------
        bug_report   : Cleaned combined text of the submitted bug.
        similar_bugs : Top-K results from RetrievalAgent.retrieve().

        Returns
        -------
        str  Markdown-formatted fix advisory.
        """
        logger.warning("FixAdvisorAgent.advise() called — returning placeholder.")
        return PLACEHOLDER_ADVISORY

    def build_prompt(
        self,
        bug_report:  str,
        similar_bugs: list[dict[str, Any]],
    ) -> str:
        """
        [Phase 2] Build the RAG prompt string (stub).

        Returns
        -------
        str  Formatted prompt ready for the LLM.
        """
        logger.error(_PLACEHOLDER_MSG)
        raise NotImplementedError(_PLACEHOLDER_MSG)

    def get_model_info(self) -> dict[str, Any]:
        """Return metadata about the configured LLM (stub)."""
        return {
            "model_name": self.model_name,
            "status":     "not_connected",
            "phase":      2,
            "provider":   "Google Gemini (planned)",
        }
