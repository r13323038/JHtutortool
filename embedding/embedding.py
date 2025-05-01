# embedding.py (OpenAI SDK v1.x 正確版：支援本地/.env與Cloud Run)

import os
from openai import OpenAI

# 嘗試從環境變數讀取
api_key = os.getenv("OPENAI_API_KEY")

# 本地開發時，允許從 .env 補救
if not api_key and os.path.exists(".env"):
    from dotenv import dotenv_values
    env_vars = dotenv_values(".env")
    api_key = env_vars.get("OPENAI_API_KEY")

# 若還是沒有，則拋錯
if not api_key:
    raise RuntimeError("❌ 環境變數 OPENAI_API_KEY 沒設定，請檢查 Cloud Run 或本地設定")

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=api_key)

EMBEDDING_MODEL = "text-embedding-3-small"

def get_embedding(text: str) -> list[float]:
    """
    將輸入文字轉為語意向量
    """
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print("[Embedding Error]", e)
        return []
