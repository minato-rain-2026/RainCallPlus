import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "38848f06536b1d42a209867990146039"

# エリアごとの座標データ
AREAS = {
    "higashihiroshima": {"name": "東広島市", "lat": "34.399", "lon": "132.744"},
    "hiroshima": {"name": "広島市", "lat": "34.385", "lon": "132.455"},
    "tokyo": {"name": "東京都", "lat": "35.689", "lon": "139.691"}
}

@app.route('/')
def index():
    # ユーザーが選んだエリアを取得（選んでない時は東広島）
    area_id = request.args.get('area', 'higashihiroshima')
    area_info = AREAS.get(area_id, AREAS['higashihiroshima'])
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={area_info['lat']}&lon={area_info['lon']}&appid={API_KEY}&units=metric&lang=ja"
    
    try:
        res = requests.get(url, timeout=5).json()
        pop = int(res['list'][0].get('pop', 0) * 100)
        msg = "傘が必要です" if pop >= 30 else "傘は不要です"
        return render_template('index.html', city=area_info['name'], pop=pop, message=msg)
    except:
        return render_template('index.html', city=area_info['name'], pop="--", message="データ取得中...")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))