# prompt_engine.py

def generate_prompt(user_question: str, knowledge_list: list[dict]) -> str:
    """
    將使用者問題與 top_k 知識點包裝成 GPT Prompt
    """

    intro = ("請對以下內容進行回答")


    question_block = f"\n學生問題：\n{user_question.strip()}"

    knowledge_blocks = []
    # for i, k in enumerate(knowledge_list):
        # block = f"\n【知識點 {i+1}】\n標題：{k.get('title', '(無)')}\n說明：{k.get('description', '(無)')}\n例題：{k.get('example', '(無)')}"
        # knowledge_blocks.append(block)

    # full_prompt = intro + question_block + "\n\n參考知識點：" + "".join(knowledge_blocks)
    full_prompt = intro + question_block + "\n\n參考知識點："

    return full_prompt


if __name__ == "__main__":
    # 測試用範例
    q = "為什麼要學一次函數？"
    top3 = [
        {"title": "一次函數", "description": "一次函數是形如 y = ax + b 的函數。", "example": "y = 2x + 1"},
        {"title": "比例式", "description": "a:b = c:d 稱為比例式。", "example": "2:3 = 4:6"},
        {"title": "二元一次", "description": "ax+by=c 為二元一次式。", "example": "2x+3y=6"}
    ]
    prompt = generate_prompt(q, top3)
    print(prompt)