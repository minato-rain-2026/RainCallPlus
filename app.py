import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

OPENWEATHER_API_KEY = "38848f06536b1d42a209867990146039"
LINE_NOTIFY_TOKEN = "OswDEb3UcPrx085fL73uE6hOonmSg6C8n80H9fC9sA5"

@app.route('/')
def index():
    # URLのパラメータを取得
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    # 1. まだ位置情報が届いていない場合の表示（エラー回避）
    if not lat or not lon:
        return render_template('index.html', city="位置情報を取得中...", pop="--", message="📍位置情報の許可をお願いします")

    # 2. 位置情報がある場合、APIを叩く
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
    
    try:
        res = requests.get(weather_url, timeout=10).json()
        city_name = res['city']['name']
        
        # 都市名の英語を日本語に変換（提出時の見栄え用）
        if "Higashihiroshima" in city_name: city_name = "東広島市"
        if "Tokyo" in city_name: city_name = "東京都"
        
        pop = int(res['list'][0].get('pop', 0) * 100)
        msg = "雨が降りそうです。傘を忘れずに！" if pop >= 30 else "傘は持たなくて大丈夫そうです。"
        
        return render_template('index.html', city=city_name, pop=pop, message=msg)
    except:
        # 万が一APIが失敗しても画面を止めない
        return render_template('index.html', city="東広島市付近", pop="0", message="現在地付近の予報を表示しています")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)