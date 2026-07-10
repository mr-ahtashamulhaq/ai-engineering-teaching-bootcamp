# RAG Assistant — AI Bootcamp Capstone

A three-mode question-answering system built with LangChain, LangGraph, FastAPI, and Groq.

## Project Structure

```
week-4/
├── capstone.ipynb     # Teaching notebook — run this first to understand the pipeline
├── ingestion.py       # CLI: embed a PDF and save a FAISS index
├── rag.py             # Module: get_answer(question) → {answer, sources}
├── agent.py           # LangGraph web-search agent (mode 3)
├── main.py            # FastAPI server — four endpoints
├── index.html         # Single-file chat UI
├── requirements.txt
├── .env               # API keys (never commit this)
└── deployment.md      # Railway + Vercel instructions
```

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env` and fill in your keys:

```
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly-...
```

## Usage

### Option A — CLI ingestion (then run the API)

```bash
# 1. Ingest a PDF
python ingestion.py --file your_document.pdf

# 2. Start the API
uvicorn main:app --reload

# 3. Open index.html in a browser (double-click or use Live Server)
```

### Option B — Upload via the UI

Start the API first, then upload a PDF directly from the sidebar in `index.html`.

## Three Modes

| Mode | What it does |
|------|-------------|
| **1 — Document Only** | Answers strictly from the uploaded PDF. No outside knowledge. |
| **2 — Document + AI Knowledge** | Uses the document first; supplements with general knowledge when the document is insufficient. Prefixes additions with "From general knowledge:". |
| **3 — Web Search** | Ignores any local document. Uses Tavily to fetch live search results, then answers with Groq. |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/index-status` | Returns `{"indexed": true/false}` |
| `POST` | `/ingest` | Upload a PDF (multipart form), returns `{"status":"ok","chunks":N}` |
| `POST` | `/ask` | `{"question": str, "mode": 1\|2\|3}` → `{"answer": str, "sources": [...]}` |

## Tech Stack

- **LLM** — Groq (`llama-3.3-70b-versatile`)
- **Embeddings** — HuggingFace `all-MiniLM-L6-v2` (local, no API key needed)
- **Vector store** — FAISS (local disk)
- **Agent** — LangGraph (two-node graph for web search)
- **Web search** — Tavily
- **API** — FastAPI + Uvicorn
- **Frontend** — Vanilla HTML/CSS/JS (no build step)
