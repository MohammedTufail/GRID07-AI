import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

from config import BOT_PERSONAS, SIMILARITY_THRESHOLD


EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
_embed_model: SentenceTransformer | None = None


def _get_embed_model() -> SentenceTransformer:
    global _embed_model
    if _embed_model is None:
        print(f"[Router] Loading embedding model '{EMBED_MODEL_NAME}' …")
        _embed_model = SentenceTransformer(EMBED_MODEL_NAME)
        print("[Router] Embedding model loaded ✓")
    return _embed_model


def _embed(text: str) -> list[float]:
    model = _get_embed_model()
    return model.encode(text, normalize_embeddings=True).tolist()


# ── ChromaDB in-memory collection ─────────────────────────────────────────────
from typing import Optional

_chroma_client: Optional[chromadb.Client] = None
_collection: Optional[chromadb.Collection] = None
COLLECTION_NAME = "bot_personas"


def _get_collection() -> chromadb.Collection:

    global _chroma_client, _collection

    if _collection is not None:
        return _collection

    # In-memory client — no data is persisted between process restarts.
    _chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))

    # Use cosine distance space so similarity = 1 − distance.
    _collection = _chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Upsert persona embeddings only if the collection is empty.
    if _collection.count() == 0:
        print("[Router] Embedding and storing bot personas …")
        for bot_id, persona in BOT_PERSONAS.items():
            embedding = _embed(persona["description"])
            _collection.upsert(
                ids=[bot_id],
                embeddings=[embedding],
                documents=[persona["description"]],
                metadatas=[{"name": persona["name"]}],
            )
            print(f"  ✓  {bot_id} ({persona['name']}) stored")
        print("[Router] All personas indexed ✓\n")

    return _collection


# ── Public API ─────────────────────────────────────────────────────────────────

def route_post_to_bots(
    post_content: str,
    threshold: float = SIMILARITY_THRESHOLD,
) -> list[dict]:
   
    collection = _get_collection()

    post_embedding = _embed(post_content)

    # Query all three bots (n_results = total personas).
    results = collection.query(
        query_embeddings=[post_embedding],
        n_results=len(BOT_PERSONAS),
        include=["distances", "metadatas"],
    )

    matched_bots: list[dict] = []

    distances = results["distances"][0]        # distance for each result
    ids       = results["ids"][0]              # bot_id strings
    metadatas = results["metadatas"][0]        # {"name": ...}

    for bot_id, distance, meta in zip(ids, distances, metadatas):
        # ChromaDB cosine distance: distance = 1 − similarity
        similarity = round(1.0 - distance, 4)
        print(
            f"  [Router] {bot_id} ({meta['name']}) → "
            f"similarity={similarity:.4f}  {'✅ MATCHED' if similarity >= threshold else '❌ below threshold'}"
        )
        if similarity >= threshold:
            matched_bots.append(
                {
                    "bot_id": bot_id,
                    "name": meta["name"],
                    "similarity": similarity,
                }
            )

    # Sort by similarity descending so the closest match is first.
    matched_bots.sort(key=lambda x: x["similarity"], reverse=True)
    return matched_bots


# ── CLI demo ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_posts = [
        "OpenAI just released a new model that might replace junior developers.",
        "Bitcoin hits a new all-time high as institutional investors pile in.",
        "Big Tech companies are lobbying against privacy laws to harvest more data.",
        "The Federal Reserve raises interest rates by 50 basis points.",
        "SpaceX successfully launches another Starship prototype.",
    ]

    for post in test_posts:
        print("=" * 70)
        print(f"📨 POST: {post}")
        print("-" * 70)
        matched = route_post_to_bots(post)
        if matched:
            print(f"\n Routed to {len(matched)} bot(s):")
            for bot in matched:
                print(f"   → {bot['bot_id']} ({bot['name']})  sim={bot['similarity']:.4f}")
        else:
            print("  ⚠️  No bots matched (all below threshold).")
        print()