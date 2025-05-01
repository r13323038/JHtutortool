# inspect_chroma.py

from chromadb import PersistentClient
from chromadb.config import Settings
import pprint

CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "knowledge"

client = PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_collection(name=COLLECTION_NAME)

# 取得所有向量條目
entries = collection.get(include=["embeddings", "metadatas", "documents"])

ids = entries.get("ids") or []
docs = entries.get("documents") or []
metas = entries.get("metadatas") or []
embeds = entries.get("embeddings") or []

print("\n📋 當前 ChromaDB 向量庫內容：")
print("─" * 50)
for i in range(len(ids)):
    doc_id = ids[i] if i < len(ids) else "(無)"
    doc = docs[i] if i < len(docs) and docs[i] is not None else "(無)"
    meta = metas[i] if i < len(metas) and metas[i] is not None else {}
    embed = embeds[i] if i < len(embeds) else None
    vec_preview = embed[:5] if isinstance(embed, list) else "❌ 無向量"

    print(f"🆔 {doc_id}\n📄 問法：{meta.get('question', doc)}\n🔖 原始知識 ID：{meta.get('source_id', '(無)')}\n🔢 向量前 5 維：{vec_preview}\n")

print(f"✅ 共列出 {len(ids)} 筆向量資料")
