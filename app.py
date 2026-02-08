import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- 画像から救出したあなたの設定 ---
LINE_ACCESS_TOKEN = 'OswDEb3UcLCFberdDbl9YlJym+3i0X5RAppdK2qBGtDn8c85EpHNw/qcG+maHGUoI7E4V9BwiLX85dC7eKKCkIZjhtf2dyx6BVJmIRwfZCpxmpjHDFaBQTYVM+bb1i/Xt04cJ1RfpQ80nGlavV9/GgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '636eae7868c323472e17f003e48b816c'
OPENWEATHER_API_KEY = 'dcb2c4d8af0212f468f270bfcdc1dccf'

def send_line_notification(pop, city):
    """LINEに通知を送るメイン機能"""
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "messages": [
            {
                "type": "text",
                "text": f"【RainCall+】\n{city}の降水確率は {pop}% だよ！☔\n傘が必要かもしれません。"
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"LINE通知送信結果: {response.status_code}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

@app.route('/')
def index():
@app.route('/')
def index():
    # ★ここ！送られてきた座標があれば使い、なければ東京にする設定
    lat = request.args.get('lat', '35.6895')
    lon = request.args.get('lon', '139.6917')

    # 天気予報を取得するURL（必ず上のlat, lonを使うようにする）
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
    
    # 読み取った lat と lon を使って天気を検索する
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
    pop = 0
    city = "位置情報を取得中..."
    message = "位置情報を許可してね"

    try:
        res = requests.get(weather_url).json()
        if res.get('list'):
            # 降水確率をパーセント表示に変換
            pop = int(res['list'][0].get('pop', 0) * 100)
            city = res['city']['name']
            
            # 降水確率が30%以上ならLINEを送る
            if pop >= 30:
                message = "傘を持って出かけよう！"
                send_line_notification(pop, city)
            else:
                message = "今日は傘は不要そうだよ。"
    except:
        city = "データ取得エラー"

    return render_template('index.html', pop=pop, city=city, message=message)

if __name__ == '__main__':
    # Renderのポート設定に対応させる
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)