import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# あなたのAPIキーとトークン
OPENWEATHER_API_KEY = "38848f06536b1d42a209867990146039"
LINE_NOTIFY_TOKEN = "OswDEb3UcPrx085fL73uE6hOonmSg6C8n80H9fC9sA5"

def send_line_notify(message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
    data = {'message': message}
    requests.post(line_notify_api, headers=headers, data=data)

@app.route('/')
def index():
    # URLから現在地を取得（なければ東京）
    lat = request.args.get('lat', '35.6895')
    lon = request.args.get('lon', '139.6917')
    
    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ja"
    res = requests.get(weather_url).json()
    
    city = res['city']['name']
    first_forecast = res['list'][0]
    pop = int(first_forecast.get('pop', 0) * 100)
    
    if pop >= 30:
        message = f"【RainCall+】{city}の降水確率は{pop}%です。傘を忘れずに！"
        send_line_notify(message)
        msg_text = "雨が降りそうです。LINEを送りました！"
    else:
        msg_text = "傘は持たなくて大丈夫そうです。"

    return render_template('index.html', city=city, pop=pop, message=msg_text)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)