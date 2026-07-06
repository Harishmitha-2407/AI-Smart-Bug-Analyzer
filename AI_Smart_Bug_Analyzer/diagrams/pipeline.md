# Pipeline Diagrams

All diagrams use [Mermaid](https://mermaid.js.org/) syntax.
Render them in any Mermaid-compatible viewer (GitHub, VS Code extension, mermaid.live).

## Full pipeline (both phases)

```mermaid
flowchart TD
    U([👤 Developer]) -->|Text or log file| SUB

    subgraph SUB ["Bug Submission — ✅ Phase 1"]
        S1[Accept inputs]
        S2[Validate]
        S3[Merge & Build BugReport]
        S1 --> S2 --> S3
    end

    subgraph PRE ["Preprocessing — ✅ Phase 1"]
        P1[Lowercase]
        P2[Strip HTML & URLs]
        P3[Remove punctuation]
        P4[Collapse whitespace]
        P1-->P2-->P3-->P4
    end

    subgraph STO ["Storage — ✅ Phase 1"]
        CSV[(bug_dataset.csv)]
        LOG[(uploaded_logs/)]
    end

    subgraph EMB ["Embedding — 🔒 Phase 2"]
        E1[Load SentenceTransformer]
        E2[Encode text → vector]
        E1 --> E2
    end

    subgraph RET ["Retrieval — 🔒 Phase 2"]
        R1[Query ChromaDB]
        R2[Return top-K matches]
        R1 --> R2
    end

    subgraph FIX ["Fix Advisory — 🔒 Phase 2"]
        F1[Build RAG prompt]
        F2[Call Gemini API]
        F3[Parse & return advisory]
        F1-->F2-->F3
    end

    SUB --> PRE --> STO
    STO --> EMB --> RET --> FIX
    FIX --> UI[✅ Results in Streamlit]

    style EMB fill:#1a1a2a,stroke:#3a3a6a,color:#888
    style RET fill:#1a1a2a,stroke:#3a3a6a,color:#888
    style FIX fill:#1a1a2a,stroke:#3a3a6a,color:#888
```
