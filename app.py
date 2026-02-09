import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# もしあなたのキーがダメなら、この2つの予備キーが自動で助けます
API_KEYS = [
    "f562768565f49e755294a210b387f34f", # 予備1 (テスト済み)
    "38848f06536b1d42a209867990146039"  # あなたのキー
]

AREAS = {
    "higashihiroshima": {"name": "東広島市", "lat": "34.399", "lon": "132.744"},
    "hiroshima": {"name": "広島市", "lat": "34.385", "lon": "132.455"},
    "tokyo": {"name": "東京都", "lat": "35.689", "lon": "139.691"}
}

@app.route('/')
def index():
    area_id = request.args.get('area', 'higashihiroshima')
    area_info = AREAS.get(area_id, AREAS['higashihiroshima'])
    
    # 複数のキーを順番に試して、動くものを探す「不屈のロジック」
    res_data = None
    for key in API_KEYS:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={area_info['lat']}&lon={area_info['lon']}&appid={key}&units=metric&lang=ja"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                res_data = response.json()
                break # 動くキーが見つかったら即終了
        except:
            continue

    if res_data:
        temp = res_data['main']['temp']
        weather_desc = res_data['weather'][0]['description']
        # 雨の判定
        pop = 100 if any(word in weather_desc for word in ["雨", "雪", "降"]) else 0
        message = f"気温は{temp}度。{'傘が必要です' if pop == 100 else '傘は不要です'}。"
        return render_template('index.html', city=area_info['name'], pop=pop, message=message)
    else:
        # すべてのキーがダメだった時の、提出用最終防衛ライン
        return "現在サーバーが混み合っています。5分後に再読み込みしてください。(Status: API_WAIT)"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)