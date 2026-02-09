import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    # スマホから届いた座標を受け取る
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    # まだ届いていない時は「取得中」と出す
    if not lat:
        return '<html><body><p>位置情報を取得しています...</p><script>navigator.geolocation.getCurrentPosition(p=>location.href="/?lat="+p.coords.latitude+"&lon="+p.coords.longitude);</script></body></html>'

    # 届いたら天気を取る
    api_key = "38848f06536b1d42a209867990146039"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=ja"
    
    try:
        data = requests.get(url).json()
        temp = data['main']['temp']
        # 東広島かどうかを判定
        city = "東広島市付近" if "34.3" in lat else data.get('name', '現在地')
        return f"<h1>📍{city}</h1><p>気温: {temp}度</p><p>この画面が表示されれば位置情報連携は成功です。</p>"
    except:
        return "データ取得中...ページを更新してください。"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    