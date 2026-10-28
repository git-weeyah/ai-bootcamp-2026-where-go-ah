import streamlit as st
from openai import OpenAI

CHAT_MODEL = "gpt-4o-mini"
EMBED_MODEL = "text-embedding-3-small"


@st.cache_resource
def _client() -> OpenAI:
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def embed(texts: list[str]) -> list[list[float]]:
    out: list[list[float]] = []
    for i in range(0, len(texts), 100):
        resp = _client().embeddings.create(model=EMBED_MODEL, input=texts[i : i + 100])
        out.extend(d.embedding for d in resp.data)
    return out


def chat(system: str, user: str) -> str:
    resp = _client().chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return resp.choices[0].message.content or ""
