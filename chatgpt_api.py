# chatgpt_api.py (OpenAI SDK v1.x 正確版)

import os
from openai import OpenAI

# 嘗試從環境變數讀取
api_key = os.getenv("OPENAI_API_KEY")

# 本地開發時允許從 .env 補救
if not api_key and os.path.exists(".env"):
    from dotenv import dotenv_values
    env_vars = dotenv_values(".env")
    api_key = env_vars.get("OPENAI_API_KEY")

# 若還是沒有，則拋錯
if not api_key:
    raise RuntimeError("❌ 環境變數 OPENAI_API_KEY 沒設定，請確認環境變數。")

client = OpenAI(api_key=api_key)

CHAT_MODEL = "gpt-4.1-nano-2025-04-14"

system_prompt = (
    "你是一位親切、耐心且擅長教學的國中老師。你即將回答一位學生的提問，"
    "請務必以正確為首要原則，並使用國中生能理解的方式解釋。\n"
    "請確保你的回答都是繁體中文，且符合中華民國（台灣）所使用的字彙與在地化文法\n"
    "若學生的問題與學科內容無關，請以老師的身份，考量學生的年齡與成熟度，"
    "給予得體、適當又有教育意義的回答。\n"
    "由於你會以訊息的方式回答學生，所以請不要以任何markdown形式回答"
)

def ask_gpt(prompt: str) -> str:
    """
    傳入 prompt，取得 GPT 回答內容
    """
    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[ChatGPT API Error]", e)
        return "❌ 發生錯誤，無法取得回答。"
