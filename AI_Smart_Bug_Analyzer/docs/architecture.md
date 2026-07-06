# System Architecture & Data Flow

## 1. Overall System Architecture

```mermaid
graph TB
    subgraph UI ["🖥️ Streamlit UI (app.py)"]
        S[Sidebar\nKB stats · Settings]
        I[Input Panel\nText area · File uploader]
        R[Results Panel\nBug info · Advisory]
    end

    subgraph Agents ["🤖 Agent Layer"]
        A1[SubmissionAgent\n✅ Phase 1]
        A2[PreprocessingAgent\n✅ Phase 1]
        A3[EmbeddingAgent\n🔒 Phase 2]
        A4[RetrievalAgent\n🔒 Phase 2]
        A5[FixAdvisorAgent\n🔒 Phase 2]
    end

    subgraph Utils ["🔧 Utilities"]
        V[Validator]
        C[Cleaner]
        F[FileHandler]
        L[Logger]
    end

    subgraph Storage ["💾 Storage"]
        CSV[(bug_dataset.csv)]
        UPL[(uploaded_logs/)]
        VDB[(ChromaDB\n🔒 Phase 2)]
    end

    subgraph External ["☁️ External — Phase 2"]
        G[Google Gemini API]
        ST[SentenceTransformers]
    end

    I --> A1
    A1 --> V
    A1 --> F
    A1 --> A2
    A2 --> C
    A2 --> A3
    A3 --> ST
    A3 --> A4
    A4 --> VDB
    A4 --> A5
    A5 --> G
    A5 --> R
    F --> CSV
    F --> UPL

    style A3 fill:#1a1a2a,stroke:#3a3a6a
    style A4 fill:#1a1a2a,stroke:#3a3a6a
    style A5 fill:#1a1a2a,stroke:#3a3a6a
    style VDB fill:#1a1a2a,stroke:#3a3a6a
    style G fill:#1a1a2a,stroke:#3a3a6a
    style ST fill:#1a1a2a,stroke:#3a3a6a
```

---

## 2. Data Flow Diagram

```mermaid
flowchart LR
    U([👤 User]) -->|description + log file| SM

    subgraph SM ["Bug Submission Module"]
        direction TB
        V1[Validate description]
        V2[Validate file type/size]
        V3[Check not both empty]
        V1 --> V3
        V2 --> V3
    end

    SM -->|invalid| ERR[❌ Error shown in UI]
    SM -->|valid| PP

    subgraph PP ["Preprocessing"]
        P1[Lowercase]
        P2[Strip HTML]
        P3[Remove punctuation]
        P4[Collapse whitespace]
        P1 --> P2 --> P3 --> P4
    end

    PP --> TS

    subgraph TS ["Temporary Storage ✅"]
        CSV[(bug_dataset.csv)]
        LOG[(uploaded_logs/)]
    end

    TS --> PH

    subgraph PH ["Future AI Pipeline 🔒"]
        E[Embed text]
        Q[Query ChromaDB]
        G[Generate fix\nvia Gemini]
        E --> Q --> G
    end

    PH --> UI[✅ Results displayed]

    style ERR fill:#4d0000,color:#fff
    style PH fill:#1a1a2a,stroke:#3a3a6a,color:#888
```

---

## 3. Component Interaction Diagram

```mermaid
sequenceDiagram
    actor U as User
    participant UI as Streamlit UI
    participant SA as SubmissionAgent
    participant VL as Validator
    participant FH as FileHandler
    participant PA as PreprocessingAgent
    participant CL as Cleaner
    participant CSV as bug_dataset.csv

    U->>UI: Enter description + upload log
    U->>UI: Click "Submit Bug"
    UI->>SA: submit(description, log_bytes, filename)
    SA->>VL: validate_description(text)
    SA->>VL: validate_file(filename, size)
    SA->>VL: validate_submission(desc, has_file)
    VL-->>SA: ✅ valid
    SA->>FH: save_upload(filename, bytes)
    FH-->>SA: saved_path
    SA->>FH: read_upload(saved_path)
    FH-->>SA: log_text
    SA-->>UI: BugReport(bug_id, timestamp, …)
    UI->>PA: process(report)
    PA->>CL: clean(description)
    PA->>CL: clean_log(log_text)
    CL-->>PA: cleaned texts
    PA-->>UI: {clean_description, clean_log}
    UI->>FH: append_to_csv(row)
    FH->>CSV: write row
    UI-->>U: ✅ Success — Bug ID shown
```

---

## 4. User Workflow Diagram

```mermaid
flowchart TD
    START([Open app.py in browser]) --> LAND[Landing page with\nhero banner + empty form]
    LAND --> INP{Choose input method}

    INP -->|Text| TA[Paste bug description\nin text area]
    INP -->|File| UPL[Upload .txt or .log file]
    INP -->|Both| BOTH[Paste description\nAND upload file]

    TA --> SUBMIT
    UPL --> SUBMIT
    BOTH --> SUBMIT

    SUBMIT[Click Submit Bug button] --> VAL{Validation}
    VAL -->|Empty input| WARN[⚠️ Warning message\nshown inline]
    VAL -->|File too large| ERR[❌ Error message\nshown inline]
    VAL -->|Invalid file type| ERR
    VAL -->|Valid| PROC[Preprocessing\nspinner shown]

    PROC --> SAVE[Save to CSV\nand uploaded_logs/]
    SAVE --> SHOW[✅ Success panel\nBug ID · Timestamp · Source]
    SHOW --> ADV[Placeholder advisory\nPhase 2 coming soon]

    WARN --> INP
    ERR --> INP
    ADV --> RESET{Reset?}
    RESET -->|Click Reset| LAND
    RESET -->|Submit another| INP
```

---

## 5. Component Descriptions

| Component | Phase | Responsibility |
|---|---|---|
| `app.py` | ✅ 1 | Streamlit UI — input, validation feedback, results display |
| `SubmissionAgent` | ✅ 1 | Accept, validate, merge, and persist bug inputs |
| `PreprocessingAgent` | ✅ 1 | Clean text for downstream processing |
| `EmbeddingAgent` | 🔒 2 | Convert text to dense vectors |
| `RetrievalAgent` | 🔒 2 | Semantic search in ChromaDB |
| `FixAdvisorAgent` | 🔒 2 | RAG prompt + Gemini response |
| `Validator` | ✅ 1 | Input validation with typed exceptions |
| `Cleaner` | ✅ 1 | Text normalisation pipeline |
| `FileHandler` | ✅ 1 | File I/O and CSV persistence |
| `Logger` | ✅ 1 | Centralised structured logging |
| `bug_dataset.csv` | ✅ 1 | Flat-file storage for submitted bugs |
| `ChromaDB` | 🔒 2 | Vector store for semantic retrieval |
