from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI
import os

app = Flask(__name__)

# 從環境變數讀取金鑰（如果沒有則使用預設值）
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET', 'YOUR_LINE_CHANNEL_SECRET')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')

# 初始化 LINE Bot API 和 Webhook Handler
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 初始化 OpenAI Client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature header
    signature = request.headers['X-Line-Signature']
    
    # 取得 request body
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # 驗證簽章
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    # 檢查是否以半形句點開頭
    if user_message.startswith('.'):
        # 僅移除第一個字元（index 0），保留後面所有內容
        ai_input = user_message[1:]
        
        # 呼叫 OpenAI API
        try:
            response = openai_client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "user", "content": ai_input}
                ]
            )
            
            ai_response = response.choices[0].message.content
            
            # 透過 LINE Reply API 回覆
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=ai_response)
            )
        except Exception as e:
            app.logger.error(f"OpenAI API Error: {str(e)}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，AI 處理時發生錯誤。")
            )

@app.route("/", methods=['GET'])
def home():
    return "LINE Bot Webhook is running!"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
