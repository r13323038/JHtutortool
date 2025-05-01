# main.py

import os
import json
import uuid
from datetime import datetime
from search_knowledge import search_knowledge
from prompt_engine import generate_prompt
from chatgpt_api import ask_gpt

LOG_FILE = "log.json"

def save_log(data: dict):
    """儲存一筆問答記錄到 log.json"""
    existing = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except:
                existing = []

    existing.append(data)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

def main():
    question = input("請輸入你的問題：\n> ").strip()
    if not question:
        print("❌ 問題不可為空")
        return

    try:
        top_knowledge = search_knowledge(question, top_k=3)

        if not top_knowledge:
            print("⚠️ 找不到相關知識點，請嘗試其他問題。")
            return

        prompt = generate_prompt(question, top_knowledge)
        print("\n📦 產生的提示語：")
        print(prompt)

        print("\n⏳ 等待 GPT 回答中...")
        response = ask_gpt(prompt)

        print("\n🧠 GPT 老師的回答：")
        print(response)

        # 儲存 log
        entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "matched_ids": [k["id"] for k in top_knowledge],
            "prompt": prompt,
            "response": response
        }
        save_log(entry)

    except Exception as e:
        print("❌ 發生錯誤：", e)


if __name__ == "__main__":
    main()
