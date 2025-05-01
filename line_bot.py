# line_bot.py (修改後)

import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from search_knowledge import search_knowledge
from prompt_engine import generate_prompt
from chatgpt_api import ask_gpt

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise EnvironmentError("Please set LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET.")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()

    knowledge = search_knowledge(user_text)
    prompt = generate_prompt(user_text, knowledge)
    reply = ask_gpt(prompt)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

    log_interaction(user_text, knowledge, reply)

# ✅ 改成空函式，避免寫硬碟失敗
def log_interaction(question, knowledge, answer):
    pass

# ✅ 最重要：確保監聽 0.0.0.0:8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Health Check
@app.route("/ping", methods=["GET"])
def ping():
    return "pong"