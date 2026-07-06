"""
app.py — AI Smart Bug Analyzer & Fix Advisor
Phase 1 (Tasks 1-5): Bug Submission Module

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
from pathlib import Path

import config
from agents.submission_agent import SubmissionAgent
from agents.preprocessing_agent import PreprocessingAgent
from agents.fix_advisor_agent import PLACEHOLDER_ADVISORY
from utils.validator import (
    ValidationError, EmptyInputError,
    DescriptionTooLongError, InvalidFileTypeError, FileTooLargeError,
)
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b2a3b 50%, #0f3460 100%);
    border-radius: 14px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.4rem;
    color: #fff;
}
.hero h1 { font-size: 1.9rem; font-weight: 700; margin: 0 0 .35rem; }
.hero p  { font-size: .95rem; color: #a0b4cc; margin: 0; }
.hero .phase-badge {
    display: inline-block;
    background: #1a4a1a;
    color: #66ffaa;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: .75rem;
    font-weight: 600;
    margin-top: .6rem;
}

.stat-card {
    background: #0e1117;
    border: 1px solid #1e2a3a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.stat-label { font-size: .75rem; color: #8899aa; margin-bottom: 4px; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: #e0e8f0; }

.char-counter { font-size: .78rem; text-align: right; margin-top: 2px; }
.char-ok   { color: #66ffaa; }
.char-warn { color: #ffe066; }
.char-over { color: #ff6b6b; }

.bug-card {
    background: #060d18;
    border: 1px solid #1e3a5a;
    border-left: 4px solid #4fc3f7;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-top: .8rem;
}
.bug-id   { font-size: 1.1rem; font-weight: 700; color: #4fc3f7; }
.bug-meta { font-size: .8rem; color: #8899aa; margin-top: 4px; }

.phase2-box {
    background: #0a0a16;
    border: 1px dashed #3a3a6a;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    color: #6677aa;
    font-size: .88rem;
}

#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _csv_row_count() -> int:
    """Return number of data rows in bug_dataset.csv (0 if missing)."""
    p = config.BUG_DATASET_PATH
    if not p.exists() or p.stat().st_size == 0:
        return 0
    try:
        return max(0, len(pd.read_csv(p)) )
    except Exception:
        return 0


def _char_counter_html(current: int, maximum: int) -> str:
    pct = current / maximum
    cls = "char-ok" if pct < 0.75 else "char-warn" if pct < 1.0 else "char-over"
    return f'<div class="char-counter {cls}">{current:,} / {maximum:,} characters</div>'


# ── Sidebar ────────────────────────────────────────────────────────────────────

def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(f"## {config.APP_ICON} Bug Analyzer")
        st.caption(config.APP_VERSION)
        st.divider()

        # Stats
        st.markdown("### 📊 Dataset Stats")
        total = _csv_row_count()
        st.metric("Bugs submitted", total)
        if total > 0:
            try:
                df = pd.read_csv(config.BUG_DATASET_PATH)
                open_count = (df["FixStatus"] == "Open").sum() if "FixStatus" in df.columns else "—"
                st.metric("Open bugs", open_count)
            except Exception:
                pass

        st.divider()

        # Phase status
        st.markdown("### 🗺️ Phase Status")
        st.success("✅ Phase 1 — Active")
        st.markdown("""
- ✅ Task 1 · Core Concepts Docs
- ✅ Task 2 · Architecture Docs
- ✅ Task 3 · Agent Skeletons
- ✅ Task 4 · Knowledge Base Design
- ✅ Task 5 · Submission Module
        """)
        st.divider()
        st.info("🔒 Phase 2 — Embeddings, ChromaDB, RAG & Gemini coming next.")

        st.divider()

        # Quick links
        with st.expander("📁 Project Files", expanded=False):
            st.markdown(f"**Dataset:** `{config.BUG_DATASET_PATH}`")
            st.markdown(f"**Uploads:** `{config.UPLOADED_LOGS_DIR}`")
            st.markdown("**Docs:** `docs/` folder")

        # Config info
        with st.expander("⚙️ Configuration", expanded=False):
            st.markdown(f"Max description: `{config.MAX_DESCRIPTION_CHARS:,}` chars")
            st.markdown(f"Max file size: `{config.MAX_LOG_FILE_BYTES // 1024}` KB")
            st.markdown("Allowed files: `.txt`, `.log`")

        st.divider()
        st.caption("Built with Streamlit · Python 3.11")


# ── Input form ─────────────────────────────────────────────────────────────────

def render_input_form() -> None:
    """Render the bug submission form and handle submission logic."""

    # Session-state defaults
    defaults = {
        "description": "",
        "log_bytes":   None,
        "log_filename": None,
        "submitted_report": None,
        "show_success": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    st.markdown("### 📝 Submit a Bug Report")
    st.caption("Fill in one or both fields below, then click **Submit Bug**.")

    tab_text, tab_file, tab_both = st.tabs([
        "✏️  Description",
        "📁  Upload Log File",
        "🔀  Both",
    ])

    # ── Tab 1: Description only ────────────────────────────────────────────────
    with tab_text:
        desc_val = st.text_area(
            "Bug description",
            value=st.session_state.description,
            height=180,
            placeholder=(
                "Describe the bug clearly. Include:\n"
                "• What you were doing\n"
                "• What error appeared\n"
                "• Any relevant context\n\n"
                "Example:\n"
                "  NullPointerException in UserService.getUser() at line 42 "
                "when userId is null."
            ),
            key="desc_text_tab",
            label_visibility="collapsed",
        )
        st.session_state.description = desc_val
        # Character counter
        st.markdown(
            _char_counter_html(len(desc_val), config.MAX_DESCRIPTION_CHARS),
            unsafe_allow_html=True,
        )

    # ── Tab 2: File only ───────────────────────────────────────────────────────
    with tab_file:
        uploaded = st.file_uploader(
            "Upload log file",
            type=["txt", "log"],
            help=f"Max {config.MAX_LOG_FILE_BYTES // 1024} KB · .txt or .log only",
            key="log_uploader",
            label_visibility="collapsed",
        )
        if uploaded:
            raw = uploaded.read()
            st.session_state.log_bytes    = raw
            st.session_state.log_filename = uploaded.name

            c1, c2, c3 = st.columns(3)
            c1.metric("File name", uploaded.name)
            c2.metric("File size", f"{len(raw) / 1024:.1f} KB")
            c3.metric("Type", uploaded.type or "text/plain")

            with st.expander("👁️ Preview (first 100 lines)", expanded=False):
                text_preview = raw.decode("utf-8", errors="replace")
                lines = text_preview.splitlines()[:100]
                st.code("\n".join(lines), language=None)

    # ── Tab 3: Both ────────────────────────────────────────────────────────────
    with tab_both:
        st.caption("Provide both a description and a log file for the richest analysis.")
        desc_both = st.text_area(
            "Description",
            value=st.session_state.description,
            height=130,
            key="desc_both_tab",
            label_visibility="collapsed",
            placeholder="Describe the bug here…",
        )
        st.session_state.description = desc_both
        st.markdown(
            _char_counter_html(len(desc_both), config.MAX_DESCRIPTION_CHARS),
            unsafe_allow_html=True,
        )

        uploaded_both = st.file_uploader(
            "Log file",
            type=["txt", "log"],
            key="log_uploader_both",
            label_visibility="collapsed",
        )
        if uploaded_both:
            raw = uploaded_both.read()
            st.session_state.log_bytes    = raw
            st.session_state.log_filename = uploaded_both.name
            st.caption(f"📄 `{uploaded_both.name}` · {len(raw) / 1024:.1f} KB")

    # ── Action buttons ─────────────────────────────────────────────────────────
    st.markdown("")
    b1, b2, _ = st.columns([2, 1, 4])
    submit = b1.button("🐛  Submit Bug",  type="primary",  use_container_width=True)
    reset  = b2.button("🔄  Reset Form",                   use_container_width=True)

    if reset:
        for k in ("description", "log_bytes", "log_filename",
                  "submitted_report", "show_success"):
            st.session_state[k] = None if k in ("log_bytes", "log_filename",
                                                  "submitted_report") else ""
        st.session_state.show_success = False
        st.rerun()

    if submit:
        _handle_submission()

    # ── Results ────────────────────────────────────────────────────────────────
    if st.session_state.get("show_success") and st.session_state.submitted_report:
        render_results(st.session_state.submitted_report)


# ── Submission handler ─────────────────────────────────────────────────────────

def _handle_submission() -> None:
    """Validate inputs, run agents, store result in session state."""
    agent       = SubmissionAgent()
    preprocessor = PreprocessingAgent()

    desc  = st.session_state.description or ""
    log_b = st.session_state.log_bytes
    fname = st.session_state.log_filename

    with st.spinner("Validating and submitting…"):
        try:
            report = agent.submit(
                description=desc or None,
                log_bytes=log_b,
                filename=fname,
            )
        except EmptyInputError as exc:
            st.warning(f"⚠️  {exc}")
            return
        except DescriptionTooLongError as exc:
            st.error(f"✂️  {exc}")
            return
        except (InvalidFileTypeError, FileTooLargeError) as exc:
            st.error(f"📁  {exc}")
            return
        except ValidationError as exc:
            st.error(f"❌  Validation error: {exc}")
            return
        except Exception as exc:
            st.error(f"❌  Unexpected error: {exc}")
            logger.exception("Submission error: %s", exc)
            return

    with st.spinner("Preprocessing text…"):
        cleaned = preprocessor.process(report)

    st.session_state.submitted_report = {
        "report":  report,
        "cleaned": cleaned,
    }
    st.session_state.show_success = True
    st.success(f"✅  Bug submitted successfully!  **ID: {report.bug_id}**")


# ── Results display ────────────────────────────────────────────────────────────

def render_results(payload: dict) -> None:
    report  = payload["report"]
    cleaned = payload["cleaned"]

    st.markdown("---")
    st.markdown("### ✅ Submitted Bug Report")

    # Metadata cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🆔 Bug ID",     report.bug_id)
    c2.metric("🕐 Submitted",  report.submitted_at[:10])
    c3.metric("📥 Source",     report.source.upper())
    c4.metric("📄 Log File",   report.log_filename or "—")

    # Bug card
    st.markdown(
        f'<div class="bug-card">'
        f'  <div class="bug-id">{report.bug_id}</div>'
        f'  <div class="bug-meta">Submitted: {report.submitted_at} &nbsp;·&nbsp; '
        f'Source: {report.source}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Detail columns
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("#### 📋 Description")
        if report.description:
            st.text_area(
                "desc_display",
                value=report.description,
                height=160,
                disabled=True,
                label_visibility="collapsed",
            )
            with st.expander("🧹 Cleaned preview", expanded=False):
                st.code(cleaned.get("clean_description", ""), language=None)
        else:
            st.caption("No description provided.")

    with right:
        st.markdown("#### 📄 Log File Content")
        if report.log_text:
            st.text_area(
                "log_display",
                value=report.log_text[:2000] + ("…" if len(report.log_text) > 2000 else ""),
                height=160,
                disabled=True,
                label_visibility="collapsed",
            )
            st.caption(
                f"File: `{report.log_filename}` · "
                f"{len(report.log_text):,} characters"
            )
        else:
            st.caption("No log file uploaded.")

    # Phase 2 advisory placeholder
    st.markdown("---")
    st.markdown("### 💡 AI Fix Advisory")
    st.markdown(
        f'<div class="phase2-box">{PLACEHOLDER_ADVISORY}</div>',
        unsafe_allow_html=True,
    )

    # Download advisory
    st.download_button(
        label="⬇️  Download Advisory (.md)",
        data=PLACEHOLDER_ADVISORY,
        file_name=f"{report.bug_id}_advisory.md",
        mime="text/markdown",
        use_container_width=False,
    )


# ── Dataset viewer ─────────────────────────────────────────────────────────────

def render_dataset_tab() -> None:
    st.markdown("### 📊 Bug Dataset")

    if not config.BUG_DATASET_PATH.exists():
        st.info("No bugs submitted yet. Use the **Submit Bug** tab to add one.")
        return

    try:
        df = pd.read_csv(config.BUG_DATASET_PATH)
    except Exception as exc:
        st.error(f"Could not read dataset: {exc}")
        return

    if df.empty:
        st.info("Dataset is empty. Submit your first bug above.")
        return

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        status_opts = ["All"] + sorted(df["FixStatus"].dropna().unique().tolist()) if "FixStatus" in df.columns else ["All"]
        status_f = st.selectbox("FixStatus", status_opts)
    with fc2:
        sev_opts = ["All"] + sorted(df["Severity"].dropna().unique().tolist()) if "Severity" in df.columns else ["All"]
        sev_f = st.selectbox("Severity", sev_opts)
    with fc3:
        search_q = st.text_input("🔍 Search title", placeholder="keyword…")

    filtered = df.copy()
    if status_f != "All" and "FixStatus" in filtered.columns:
        filtered = filtered[filtered["FixStatus"] == status_f]
    if sev_f != "All" and "Severity" in filtered.columns:
        filtered = filtered[filtered["Severity"] == sev_f]
    if search_q and "Title" in filtered.columns:
        filtered = filtered[filtered["Title"].str.contains(search_q, case=False, na=False)]

    st.caption(f"Showing {len(filtered)} of {len(df)} records")

    # Highlight severity column
    display_cols = [c for c in config.BUG_CSV_COLUMNS if c in filtered.columns]
    st.dataframe(
        filtered[display_cols],
        use_container_width=True,
        height=420,
    )

    st.download_button(
        "⬇️  Export CSV",
        data=filtered.to_csv(index=False),
        file_name="bug_dataset_export.csv",
        mime="text/csv",
    )


# ── Docs tab ───────────────────────────────────────────────────────────────────

def render_docs_tab() -> None:
    st.markdown("### 📚 Project Documentation")

    docs = {
        "Core Concepts":         config.BASE_DIR / "docs" / "core_concepts.md",
        "Architecture":          config.BASE_DIR / "docs" / "architecture.md",
        "Knowledge Base Schema": config.BASE_DIR / "docs" / "knowledge_base_schema.md",
        "Workflow":              config.BASE_DIR / "docs" / "workflow.md",
    }

    for title, path in docs.items():
        with st.expander(f"📄 {title}", expanded=False):
            if path.exists():
                st.markdown(path.read_text(encoding="utf-8"))
            else:
                st.warning(f"File not found: `{path}`")


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    render_sidebar()

    # Hero banner
    st.markdown(
        f"""
        <div class="hero">
            <h1>{config.APP_ICON} {config.APP_TITLE}</h1>
            <p>Submit bug reports, store them in a structured knowledge base,
               and preview the upcoming AI-powered fix advisory pipeline.</p>
            <span class="phase-badge">✅ Phase 1 Active — Tasks 1–5 Complete</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top-level tabs
    tab_submit, tab_data, tab_docs = st.tabs([
        "🐛  Submit Bug",
        "📊  Dataset Viewer",
        "📚  Documentation",
    ])

    with tab_submit:
        render_input_form()

    with tab_data:
        render_dataset_tab()

    with tab_docs:
        render_docs_tab()


if __name__ == "__main__":
    main()
