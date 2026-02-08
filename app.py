import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# APIキーとトークン（そのまま使用）
OPENWEATHER_API_KEY = "38848f06536b1d42a209867990146039"
LINE_NOTIFY_TOKEN = "OswDEb3UcPrx085fL73uE6hOonmSg6C8n80H9fC9sA5"

def send_line_notify(message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
    data = {'message': message}
    try:
        requests.post(line_notify_api, headers=headers, data=data, timeout=5)
    except:
        pass

@app.route('/')
def index():
    # URLから緯度・経度を取得
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # 座標がない場合はデフォルトで東京を表示
    if not lat or not lon:
        lat, lon = '35.6895', '139.6917'
    
    # 予報(forecast)ではなく、確実に名前が取れる現在の天気(weather)を使用
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
    
    city = "取得中..."
    pop = 0
    msg_text = "位置情報を読み取っています..."

    try:
        response = requests.get(weather_url, timeout=10)
        res = response.json()
        
        if response.status_code == 200:
            # 都市名の取得（英語名から日本語への簡易変換も含む）
            raw_name = res.get('name', '現在地')
            city_map = {"Higashihiroshima": "東広島市", "Hiroshima-shi": "広島市", "Tokyo": "東京都"}
            city = city_map.get(raw_name, raw_name)
            
            # 現在の天気から「雨」の情報を探す（popの代わりに雨量や天候で判定）
            weather_main = res.get('weather', [{}])[0].get('main', '')
            # forecast APIではないためpopは擬似的に設定、またはそのまま表示
            pop = 0 
            if "Rain" in weather_main:
                pop = 80 # 雨なら80%と表示
                msg_text = "今、雨が降っています！傘が必要です。"
                send_line_notify(f"【RainCall+】{city}で雨を検知しました。")
            else:
                msg_text = "今のところ傘は大丈夫そうです。"
        else:
            city = "接続待ち"
            msg_text = "APIキーを確認するか、少し待って更新してね。"
            
    except Exception:
        msg_text = "ネット接続を確認してください。"

    return render_template('index.html', city=city, pop=pop, message=msg_text)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)