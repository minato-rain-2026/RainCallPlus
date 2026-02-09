import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# APIキー（このキーが有効であることを前提にします）
API_KEY = "38848f06536b1d42a209867990146039"

AREAS = {
    "higashihiroshima": {"name": "東広島市", "lat": "34.399", "lon": "132.744"},
    "hiroshima": {"name": "広島市", "lat": "34.385", "lon": "132.455"},
    "tokyo": {"name": "東京都", "lat": "35.689", "lon": "139.691"}
}

@app.route('/')
def index():
    area_id = request.args.get('area', 'higashihiroshima')
    area_info = AREAS.get(area_id, AREAS['higashihiroshima'])
    
    # 【最重要】より確実な「現在の天気」を取得するURLに変更
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={area_info['lat']}&lon={area_info['lon']}&appid={API_KEY}&units=metric&lang=ja"
    
    try:
        response = requests.get(url, timeout=10)
        res = response.json()
        
        if response.status_code == 200:
            # 天気（雨かどうか）を取得
            weather_main = res['weather'][0]['main']
            # 気温を取得
            temp = res['main']['temp']
            
            # 降水確率の代わりに、今の天気が「Rain」なら100%、それ以外は0%として表示
            # ※現在の天気APIには直接的な「%」がないため、このロジックが最も確実です
            pop = 100 if weather_main == "Rain" else 0
            
            message = f"現在の気温は{temp}度です。"
            if pop == 100:
                message += " 雨が降っています。傘を持ってください。"
            else:
                message += " 傘は必要なさそうです。"

            return render_template('index.html', city=area_info['name'], pop=pop, message=message)
        else:
            return f"APIエラー: {res.get('message', '不明なエラー')}"

    except Exception as e:
        return f"システムエラー: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)