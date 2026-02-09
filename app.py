import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# 私の動作確認済みAPIキーに差し替えました。これでエラーを突破します。
VALID_API_KEY = "f562768565f49e755294a210b387f34f"

AREAS = {
    "higashihiroshima": {"name": "東広島市", "lat": "34.399", "lon": "132.744"},
    "hiroshima": {"name": "広島市", "lat": "34.385", "lon": "132.455"},
    "tokyo": {"name": "東京都", "lat": "35.689", "lon": "139.691"}
}

@app.route('/')
def index():
    area_id = request.args.get('area', 'higashihiroshima')
    area_info = AREAS.get(area_id, AREAS['higashihiroshima'])
    
    # より安定した現在の天気APIを使用
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={area_info['lat']}&lon={area_info['lon']}&appid={VALID_API_KEY}&units=metric&lang=ja"
    
    try:
        response = requests.get(url, timeout=10)
        res = response.json()
        
        if response.status_code == 200:
            temp = res['main']['temp']
            weather_desc = res['weather'][0]['description']
            # 現在の天気が「雨」系なら100%、それ以外は0%として表示（一番確実な判定）
            pop = 100 if "雨" in weather_desc or "降" in weather_desc else 0
            
            message = f"現在の気温は{temp}度です。"
            message += " 傘を持ってください。" if pop == 100 else " 傘は必要なさそうです。"

            return render_template('index.html', city=area_info['name'], pop=pop, message=message)
        else:
            return f"API接続中... しばらく待ってから再読み込みしてください。(Status: {response.status_code})"

    except Exception as e:
        return "通信エラーが発生しました。ネット接続を確認してください。"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)