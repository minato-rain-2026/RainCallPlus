import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# 設定情報
OPENWEATHER_API_KEY = "38848f06536b1d42a209867990146039"
LINE_NOTIFY_TOKEN = "OswDEb3UcPrx085fL73uE6hOonmSg6C8n80H9fC9sA5"

def send_line_notify(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    try:
        requests.post(url, headers=headers, data=data, timeout=5)
    except Exception as e:
        print(f"LINE通知エラー: {e}")

@app.route('/')
def index():
    # 1. クエリパラメータから緯度・経度を取得
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    # 位置情報がない場合は初期画面（東京）を表示
    if not lat or not lon:
        return render_template('index.html', city="位置情報を取得中...", pop="--", message="現在地を読み込んでいます...")

    # 2. OpenWeather APIから天気予報を取得
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
    
    try:
        res = requests.get(weather_url, timeout=10).json()
        city = res['city']['name']
        # 直近3時間の降水確率(pop)を取得 (0.0〜1.0)
        pop_value = res['list'][0].get('pop', 0)
        pop_percent = int(pop_value * 100)

        # 3. 降水確率に基づいた判定とLINE通知
        if pop_percent >= 30:
            msg = "雨が降りそうです。傘を忘れずに！"
            send_line_notify(f"\n【RainCall】\n{city}の降水確率は{pop_percent}%です。")
        else:
            msg = "傘は持たなくて大丈夫そうです。"

        return render_template('index.html', city=city, pop=pop_percent, message=msg)

    except Exception as e:
        return render_template('index.html', city="エラー", pop="!!", message="データの取得に失敗しました。")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)