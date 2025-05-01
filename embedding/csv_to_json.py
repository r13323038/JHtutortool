# csv_to_knowledge_json.py

import csv
import json

CSV_FILE = "knowledge.csv"
JSON_FILE = "knowledge.json"

knowledge_list = []

with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        row_id = row.get("id", "").strip()
        if not row_id:
            raise ValueError(f"❌ 第 {idx+1} 筆資料缺少 id 欄位，請於 CSV 加入唯一編號")

        knowledge = {
            "id": row_id,
            "標題": row.get("標題", "").strip(),
            "說明": row.get("說明", "").strip(),
        }
        # 加入例題（可選）
        if "例題" in row and row["例題"].strip():
            knowledge["例題"] = row["例題"].strip()

        # 加入問法（用｜分隔 → list）
        if "問法" in row and row["問法"].strip():
            questions = [q.strip() for q in row["問法"].split("｜") if q.strip()]
            knowledge["問法"] = questions

        knowledge_list.append(knowledge)

# 寫出為 JSON 檔案
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(knowledge_list, f, ensure_ascii=False, indent=2)

print(f"✅ 轉換完成：共 {len(knowledge_list)} 筆知識寫入 {JSON_FILE}")
