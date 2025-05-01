# search.py

from chromadb import PersistentClient
from embedding.embedding import get_embedding

CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "knowledge"

client = PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_collection(name=COLLECTION_NAME)

def search_similar_knowledge(question: str, top_k: int = 3):
    if not question.strip():
        raise ValueError("❌ 問題不可為空")

    embedding = get_embedding(question)
    if not embedding:
        raise RuntimeError("❌ 無法取得問題的語意向量")

    # 強制觸發 Chroma 清理未完成 batch，避免多次 add 嘗試錯誤訊息
    try:
        collection.get(ids=["dummy_force_refresh"])
    except:
        pass

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    matches = []
    for i, doc_id in enumerate(results["ids"][0]):
        match = {
            "id": doc_id,
            "question": results["documents"][0][i],
            "source_id": results["metadatas"][0][i].get("source_id"),
            "distance": results["distances"][0][i],
        }
        matches.append(match)
    return matches

if __name__ == "__main__":
    q = input("請輸入你的問題：\n> ").strip()
    try:
        results = search_similar_knowledge(q)
        print("\n🔍 搜尋結果：")
        for i, match in enumerate(results):
            print(f"#{i+1} 🆔 {match['id']} (score={match['distance']:.4f})")
            print(f"📄 問法：{match['question']}")
            print(f"📚 知識 ID：{match['source_id']}\n")
    except Exception as e:
        print("❌ 搜尋過程中發生錯誤：", e)
