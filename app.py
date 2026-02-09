import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "38848f06536b1d42a209867990146039"

# ユーザーが選択できるエリアリスト
AREAS = {
    "higashihiroshima": {"name": "東広島市", "lat": "34.399", "lon": "132.744"},
    "hiroshima": {"name": "広島市", "lat": "34.385", "lon": "132.455"},
    "tokyo": {"name": "東京都", "lat": "35.689", "lon": "139.691"}
}

@app.route('/')
def index():
    # URLから選択されたエリアを取得。未選択なら東広島
    area_id = request.args.get('area', 'higashihiroshima')
    area_info = AREAS.get(area_id, AREAS['higashihiroshima'])
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={area_info['lat']}&lon={area_info['lon']}&appid={API_KEY}&units=metric&lang=ja"
    
    city = area_info['name']
    pop = 0  # デフォルトを数字の0にする（エラー防止）
    message = "データを読み込み中..."

    try:
        res = requests.get(url, timeout=5).json()
        if 'list' in res:
            pop = int(float(res['list'][0].get('pop', 0)) * 100)
            message = "雨が降りそうです。傘を忘れずに！" if pop >= 30 else "傘は持たなくて大丈夫そうです。"
    except Exception:
        message = "予報を取得できませんでした。再度お試しください。"

    return render_template('index.html', city=city, pop=pop, message=message)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)