# search_knowledge.py

import os
import json
import logging
from chromadb import PersistentClient
from chromadb.config import Settings
from embedding.embedding import get_embedding

# 關閉 chroma log 輸出 & 禁用 index 重建
os.environ["CHROMADB_TELEMETRY"] = "0"
logging.getLogger("chromadb").setLevel(logging.ERROR)

CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "knowledge"

# 載入完整知識點資料（用來補全說明、例題）
with open("knowledge.json", "r", encoding="utf-8") as f:
    full_knowledge = {item["id"]: item for item in json.load(f)}

client = PersistentClient(
    path=CHROMA_DB_DIR,
    settings=Settings(allow_reset=False)  # 禁用資料 flush
)
collection = client.get_collection(name=COLLECTION_NAME)

def search_knowledge(question: str, top_k: int = 3):
    embedding = get_embedding(question)
    if not embedding:
        raise RuntimeError("❌ 無法取得語意向量")

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k * 3,  # 先多抓，後續聚合
        include=["documents", "metadatas", "distances"]
    )

    grouped = {}
    for i, doc_id in enumerate(results["ids"][0]):
        meta = results["metadatas"][0][i]
        source_id = meta.get("source_id")
        if source_id not in grouped:
            grouped[source_id] = {
                "score": results["distances"][0][i],
                "questions": [],
                "id": source_id,
            }
        grouped[source_id]["questions"].append(results["documents"][0][i])

    # 按距離排序後取前 top_k 筆知識點
    sorted_knowledge = sorted(grouped.values(), key=lambda x: x["score"])[:top_k]

    # 補全說明、例題，若找不到則回傳 "(無)"
    for item in sorted_knowledge:
        k = full_knowledge.get(item["id"], {})
        item["title"] = k.get("標題") or "(無)"
        item["description"] = k.get("說明") or "(無)"
        item["example"] = k.get("例題") or "(無)"

    return sorted_knowledge

if __name__ == "__main__":
    q = input("請輸入你的問題：\n> ").strip()
    try:
        results = search_knowledge(q)
        print("\n🔍 相近知識點：")
        for i, item in enumerate(results):
            print(f"#{i+1} 🧠 {item['title']} (ID: {item['id']})")
            print(f"📖 說明：{item['description']}")
            print(f"📝 例題：{item['example']}")
            print(f"🔎 問法舉例：{'｜'.join(item['questions'])}")
            print(f"🎯 相似度分數：{item['score']:.4f}\n")
    except Exception as e:
        print("❌ 發生錯誤：", e)
