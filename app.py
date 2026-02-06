from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "dcb2c4d8af0212f468f270bfcdc1dccf" # ここを自分のキーに変えてね！

@app.route('/')
def home():
    # ブラウザから送られてきた緯度(lat)と経度(lon)を受け取る
    lat = request.args.get('lat', '35.6895') # デフォルトは東京
    lon = request.args.get('lon', '139.6917')

    # 緯度・経度を使って天気を調べるURL
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    data = requests.get(url).json()
    pop = data['list'][0]['pop'] * 100
    city_name = data['city']['name'] # その場所の都市名も取得

    if pop >= 30:
        message = "今日は傘が必要だよ！☔"
    else:
        message = "傘は不要そう。いってらっしゃい！☀️"
    
    return render_template('index.html', pop=int(pop), message=message, city=city_name)
if __name__ == "__main__":
    app.run(debug=True)
