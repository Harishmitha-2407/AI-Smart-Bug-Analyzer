# 🐛 AI Smart Bug Analyzer & Fix Advisor

**Phase 1 — Tasks 1–5 Complete**

A structured, multi-agent Python application for submitting, storing, and
(in Phase 2) intelligently analysing software bugs using RAG + Gemini.

---

## What's implemented (Phase 1)

| Task | Status | Description |
|---|---|---|
| Task 1 | ✅ | Core concepts documentation (RAG, embeddings, vector search) |
| Task 2 | ✅ | System architecture & data flow diagrams |
| Task 3 | ✅ | Five agent classes (2 working + 3 stubs) |
| Task 4 | ✅ | Knowledge base schema + 20-row sample dataset |
| Task 5 | ✅ | Full Streamlit bug submission UI |

## What's coming (Phase 2)

- EmbeddingAgent — SentenceTransformers
- ChromaDB vector store + ingestion pipeline
- RetrievalAgent — semantic similarity search
- FixAdvisorAgent — Google Gemini RAG fix recommendation

---

## Project Structure

```
AI_Smart_Bug_Analyzer/
├── app.py                      # Streamlit entry point
├── config.py                   # All settings
├── requirements.txt
├── README.md
│
├── agents/
│   ├── submission_agent.py     # ✅ Full implementation
│   ├── preprocessing_agent.py  # ✅ Full implementation
│   ├── embedding_agent.py      # 🔒 Stub (Phase 2)
│   ├── retrieval_agent.py      # 🔒 Stub (Phase 2)
│   └── fix_advisor_agent.py    # 🔒 Stub (Phase 2)
│
├── data/
│   ├── bug_dataset.csv         # 20 sample bugs + user submissions
│   └── uploaded_logs/          # Saved upload files
│
├── docs/
│   ├── core_concepts.md        # RAG, embeddings, vector search explained
│   ├── architecture.md         # System + data flow diagrams
│   ├── knowledge_base_schema.md# CSV schema, JSON schema, future DB design
│   └── workflow.md             # Step-by-step phase 1 workflow
│
├── utils/
│   ├── logger.py               # Centralised logging
│   ├── cleaner.py              # Text normalisation pipeline
│   ├── validator.py            # Input validation with typed exceptions
│   └── file_handler.py         # File I/O + CSV persistence
│
└── diagrams/
    └── pipeline.md             # Mermaid pipeline diagrams
```

---

## Quick Start

### 1. Install dependencies

```bash
cd AI_Smart_Bug_Analyzer
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

### 3. Use the app

- Open the **Submit Bug** tab
- Paste a bug description and/or upload a `.log` / `.txt` file
- Click **Submit Bug**
- View the submitted report, cleaned text, and Phase 2 advisory placeholder
- Browse all submitted bugs in the **Dataset Viewer** tab
- Read project docs in the **Documentation** tab

---

## Configuration

All settings are in `config.py` — no `.env` file needed in Phase 1.

| Setting | Default | Description |
|---|---|---|
| `MAX_DESCRIPTION_CHARS` | 10 000 | Max length for pasted text |
| `MAX_LOG_FILE_BYTES` | 524 288 (512 KB) | Max uploaded file size |
| `BUG_DATASET_PATH` | `data/bug_dataset.csv` | Flat-file bug store |
| `UPLOADED_LOGS_DIR` | `data/uploaded_logs/` | Saved uploads directory |

---

## Validation Rules

| Rule | Error Type |
|---|---|
| Both inputs empty | `EmptyInputError` |
| Description > 10 000 chars | `DescriptionTooLongError` |
| File not `.txt` or `.log` | `InvalidFileTypeError` |
| File > 512 KB | `FileTooLargeError` |

---

## CSV Columns

`BugID` · `Title` · `Description` · `Module` · `Priority` · `Severity` ·
`ProgrammingLanguage` · `OperatingSystem` · `StackTrace` · `ExpectedBehavior` ·
`ActualBehavior` · `FixStatus` · `SubmittedAt` · `LogFileName`
