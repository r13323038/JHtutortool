# json_to_chroma.py

import json
import os
from chromadb import PersistentClient
from chromadb.config import Settings
from embedding import get_embedding

CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "knowledge"

# 初始化 Chroma 客戶端
client = PersistentClient(path=CHROMA_DB_DIR)

# 建立或取得 collection
if COLLECTION_NAME not in [c.name for c in client.list_collections()]:
    collection = client.create_collection(name=COLLECTION_NAME)
else:
    collection = client.get_collection(name=COLLECTION_NAME)

# 載入 JSON 知識資料
with open("knowledge.json", "r", encoding="utf-8") as f:
    knowledge_data = json.load(f)

# 取得現有 ID 避免重複
existing_ids = set()
offset = 0
while True:
    batch = collection.get(include=[], limit=1000, offset=offset)
    if not batch.get("ids"):
        break
    existing_ids.update(batch["ids"])
    offset += 1000

added_count = 0

for item in knowledge_data:
    base_id = item["id"]
    questions = item.get("問法", [])
    if isinstance(questions, str):
        questions = questions.split("｜")

    for i, q in enumerate(questions):
        doc_id = f"{base_id}-q{i}"
        if doc_id in existing_ids:
            print(f"⏩ 已存在，跳過：{doc_id}")
            continue

        embedding = get_embedding(q)
        if not embedding:
            print(f"⚠️ 無向量，跳過：{doc_id}")
            continue

        collection.add(
            ids=[doc_id],
            documents=[q],
            metadatas=[{
                "source_id": base_id,
                "title": item.get("標題", ""),
                "description": item.get("說明", ""),
                "example": item.get("例題", "")
            }],
            embeddings=[embedding]
        )
        added_count += 1
        print(f"✅ 加入：{doc_id} - {q}")

print(f"🎉 完成，共新增 {added_count} 筆問法向量")
