import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

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
    lat = request.args.get('lat', '35.6895')
    lon = request.args.get('lon', '139.6917')
    
    # 5日間/3時間ごとの予報APIを使用
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
    
    city = "取得中..."
    pop = 0
    msg_text = "位置情報を読み取っています..."

    try:
        response = requests.get(weather_url, timeout=10)
        res = response.json()
        
        if response.status_code == 200:
            # 都市名の取得を強化
            city_name = res.get('city', {}).get('name', '現在地')
            if city_name == "Higashihiroshima": city_name = "東広島市"
            if city_name == "Hiroshima-shi": city_name = "広島市"
            city = city_name
            
            # 降水確率の取得
            if 'list' in res and len(res['list']) > 0:
                first_forecast = res['list'][0]
                pop = int(first_forecast.get('pop', 0) * 100)
                
                if pop >= 30:
                    message = f"【RainCall+】{city}の降水確率は{pop}%です。傘を忘れずに！"
                    send_line_notify(message)
                    msg_text = "雨が降りそうです。LINEを送りました！"
                else:
                    msg_text = "傘は持たなくて大丈夫そうです。"
        else:
            msg_text = "データ取得エラー。更新してみてね。"
            
    except Exception:
        msg_text = "接続を確認してください。"

    return render_template('index.html', city=city, pop=pop, message=msg_text)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)