# Where Go Ah?

Streamlit RAG app that routes Singapore citizens to the right government agency/service.
Describe your situation in plain English or Singlish and the app tells you which agency and
service to go to, why, and links the official source. If the knowledge base doesn't clearly
support an answer, it says so instead of guessing.

> ⚠️ **Disclaimer:** This is **not** an official Singapore Government website and is not affiliated
> with any government agency. It is built for **educational purposes only**. Always verify
> information against the official source links and the relevant government website
> (https://www.gov.sg).

## Setup
Requires Python 3.10+ and an OpenAI API key.

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdir -p .streamlit && touch .streamlit/secrets.toml   # then add the secrets below
streamlit run app.py
```

`.streamlit/secrets.toml` (git-ignored):
```toml
OPENAI_API_KEY = "sk-..."

[APP_USERS]            # username = "password"; every page requires login
alice = "change-me"
```

The index is built automatically on first run. Use **Rebuild index** in the sidebar after editing the knowledge base.

## Pages
| Page | Purpose |
|------|---------|
| Where Go Ah? (`chat.py`) | Chat with agency filter and example questions |
| About Us | Project background |
| Methodology | Architecture, tech stack and guardrails |
| Upload Documents | Add PDF/Markdown/text files to the index (duplicates skipped by content hash) |

## Project layout
```
app.py              navigation entry point
chat.py             chat page
pages/              About Us, Methodology, Upload Documents
core/
  auth.py           session login gate (APP_USERS secret)
  llm.py            OpenAI chat + embedding wrapper
  ingest.py         parsing, chunking, indexing
  vectorstore.py    Chroma wrapper
  rag.py            retrieval, prompts, fallback
  ui.py             shared styling
knowledge_base/     curated official sources (HDB, ICA, IRAS, MSF, SPF-Traffic-Police)
sample_docs/        sample PDF for the upload page
```

## Adding to the knowledge base
Create `knowledge_base/<AGENCY>/NN-title.md` with a header block (files without `SOURCE_URL` are skipped), then click **Rebuild index**:
```
# Title

AGENCY: Immigration & Checkpoints Authority (ICA)
CATEGORY: Identity
TOPIC: Lost Singapore Identity Card
SOURCE_URL: https://www.ica.gov.sg/...
LAST_VERIFIED: 2026-10-28
```
