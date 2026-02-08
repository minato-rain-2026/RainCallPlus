import schedule
import time
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage

# --- 設定：自分のものに書き換えてください ---
API_KEY = "dcb2c4d8af0212f468f270bfcdc1dccf"
LINE_ACCESS_TOKEN = "あなたの長いアクセストークン"
# 通知したい時間を設定（例: "07:30"）
SCHEDULE_TIME = "14:56" 

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

def job():
    print(f"{SCHEDULE_TIME}になりました。天気をチェックします...")
    
    # 東京の天気をチェック（緯度・経度は必要に応じて変えてください）
    lat, lon = "35.6895", "139.6917"
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        data = requests.get(url).json()
        pop = data['list'][0]['pop'] * 100
        
        if pop >= 30:
            message = f"【傘予報】今日の降水確率は{int(pop)}%です。傘を持って行ってね！☔"
            line_bot_api.broadcast(TextSendMessage(text=message))
            print("LINEを送りました。")
        else:
            print("雨の心配はないのでLINEは見送りました。")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 時間を予約する
schedule.every().day.at(SCHEDULE_TIME).do(job)

print(f"監視を開始しました。毎日 {SCHEDULE_TIME} に通知します。")
print("※この画面（VS Code）を開いたままにしておいてくださいね。")

# ずっと見張り続ける

mport os
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    # ここにLINEのメッセージを受け取る処理を書きますが、
    # まずはRenderを「Live」にするために最小限の構成にします
    return 'OK'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)