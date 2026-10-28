import hashlib
import io
import re
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from core import llm, vectorstore

KB_DIR = Path("knowledge_base")
FIELDS = ("AGENCY", "CATEGORY", "TOPIC", "SOURCE_URL", "LAST_VERIFIED")
_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def parse_header(text: str) -> dict:
    meta = {}
    for f in FIELDS:
        m = re.search(rf"^{f}:\s*(.+)$", text, re.MULTILINE)
        meta[f.lower()] = m.group(1).strip() if m else ""
    t = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    meta["title"] = t.group(1).strip() if t else ""
    return meta


def _index(text: str, meta: dict) -> int:
    chunks = [c for c in _splitter.split_text(text) if c.strip()]
    if not chunks:
        return 0
    prefix = f"[{meta['agency']} | {meta['topic']}] " if meta.get("agency") else ""
    docs = [prefix + c for c in chunks]
    key = meta["source_file"]
    ids = [hashlib.sha1(f"{key}:{i}".encode()).hexdigest() for i in range(len(docs))]
    vectorstore.add_chunks(ids, docs, llm.embed(docs), [dict(meta) for _ in docs])
    return len(docs)


def ingest_markdown(text: str, source_file: str) -> int:
    meta = parse_header(text)
    meta["source_file"] = source_file
    return _index(text, meta)


def ingest_upload(name: str, data: bytes) -> tuple[int, str]:
    digest = hashlib.sha256(data).hexdigest()
    if vectorstore.exists_where({"content_hash": digest}):
        return 0, "duplicate"
    if name.lower().endswith(".pdf"):
        from pypdf import PdfReader

        text = "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(data)).pages)
    else:
        text = data.decode("utf-8", errors="ignore")
    if not text.strip():
        return 0, "empty"
    meta = parse_header(text)
    meta["source_file"] = f"upload/{name}"
    meta["content_hash"] = digest
    meta["title"] = meta["title"] or name
    vectorstore.delete_where({"source_file": meta["source_file"]})
    return _index(text, meta), "added"


def ingest_knowledge_base() -> int:
    total = 0
    for path in sorted(KB_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not re.search(r"^SOURCE_URL:", text, re.MULTILINE):
            continue
        total += ingest_markdown(text, str(path.relative_to(KB_DIR)))
    return total


def ensure_index() -> None:
    if vectorstore.get_collection().count() == 0:
        ingest_knowledge_base()


def rebuild_index() -> int:
    vectorstore.reset_collection()
    return ingest_knowledge_base()
