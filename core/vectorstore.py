import chromadb

COLLECTION = "where_go_ah"


def _client():
    return chromadb.PersistentClient(path="data/chroma")


def get_collection():
    return _client().get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def reset_collection():
    c = _client()
    try:
        c.delete_collection(COLLECTION)
    except Exception:
        pass
    return get_collection()


def add_chunks(ids, documents, embeddings, metadatas) -> None:
    get_collection().upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)


def query(embedding, k: int, where: dict | None = None):
    col = get_collection()
    if col.count() == 0:
        return []
    res = col.query(query_embeddings=[embedding], n_results=k, where=where)
    return [
        {"text": d, "meta": m, "distance": dist}
        for d, m, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


def delete_where(where: dict) -> None:
    get_collection().delete(where=where)


def exists_where(where: dict) -> bool:
    return bool(get_collection().get(where=where, limit=1)["ids"])
