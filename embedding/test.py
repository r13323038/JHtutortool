# test.py

from embedding.embedding import get_embedding

question = "什麼是一次函數？"

embedding = get_embedding(question)

print("✅ 向量長度：", len(embedding))
print("✅ 向量前 5 維：", embedding[:5])