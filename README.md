# 📚 智慧問答教學系統 (Learnest_Tutor)

一個結合 OpenAI 語意理解、向量資料庫、知識檢索與對話生成的教學輔助系統，協助國中生透過自然語言提問，由 GPT 給予準確、親切、在地化的回答。

---

## 📦 專案架構

```
JHtutortool/
├── main.py                # 系統進入點，整合提問、檢索、回答與紀錄
├── embedding.py          # 使用 OpenAI API 將文字轉為語意向量
├── questions_to_chroma.py # 將知識點問法與向量加入 ChromaDB
├── search_knowledge.py   # 向量比對取得最相關的知識點
├── prompt_engine.py      # 產出 GPT 提示語的模組
├── chatgpt_api.py        # 包裝與 GPT 的對話 API 呼叫
├── inspect_chroma.py     # 檢查 ChromaDB 內部內容
├── json_to_chroma.py     # 若從 JSON 匯入知識點使用
├── log.json              # 問答記錄，含問句、GPT回覆、用到的知識點
├── knowledge.json        # 儲存知識點資料的主檔案（來自 CSV 轉換）
├── requirements.txt      # 套件依賴清單
└── .env                  # 儲存 OpenAI API 金鑰
```

---

## 🧠 功能亮點

* 🔎 **語意檢索**：使用 `text-embedding-3-small` 建立知識問法向量，儲存於 ChromaDB，並查詢最相似問法。
* 💬 **提示優化**：將提問與相關知識點編成自然提示語，強化 GPT 回答聚焦與準確度。
* 📚 **教師角色設定**：GPT 以「台灣國中數學老師」為角色，語氣親切、內容正確、避免過度延伸。
* 📝 **問答紀錄**：所有使用記錄（含 prompt 與知識點 ID）皆儲存於 `log.json`，利於後續訓練與檢討。

---

## ⚙️ 使用方式

1. **建立虛擬環境**

```bash
python -m venv .venv
source .venv/bin/activate    # Windows 請改為 .venv\Scripts\activate
```

2. **安裝套件**

```bash
pip install -r requirements.txt
```

3. **放入 OpenAI 金鑰**

```
# .env
OPENAI_API_KEY=sk-xxxxx...
```

4. **準備知識點資料**
   以 CSV 格式匯入後轉為 `knowledge.json`，格式如下：

```csv
id,標題,說明,例題,問法
M00001,一次函數,一次函數是形如 y = ax + b 的函數。,y = 2x + 1,什麼是一次函數？｜一次函數是線嗎？｜y=ax+b
```

5. **執行知識點上傳**

```bash
python questions_to_chroma.py
```

6. **啟動問答主程式**

```bash
python main.py
```

---

## 🚀 未來方向

* ✅ LINE Bot 串接（使用 Webhook + GCP Cloud Functions）
* ✅ 自動擴充知識點（根據課綱與歷屆題目）
* ✅ 檢索引擎支援 BM25/TF-IDF
* ✅ 支援多階段 prompt 強化問答邏輯與答案精度
* ✅ UI 前端（Web or ChatBot 視覺化）

---

## 🤝 貢獻方式

若你也關注台灣數位教學、AI 教育應用，歡迎提交 PR、開 Issue 或參與資料整理！

---

## 📄 授權條款

本專案採用 [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/) 授權條款：

- ✅ **允許修改與分享**：你可以自由複製、修改、重新發佈本專案內容。
- ❌ **禁止商業用途**：不得將本專案或其衍生作品用於任何商業目的。
- 🔗 **需標明出處**：使用時請附上原始作者與本授權連結。

詳細條款請參考：  
https://creativecommons.org/licenses/by-nc/4.0/