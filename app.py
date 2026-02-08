import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# キーは維持しますが、エラーでも画面を止めない設定にします
OPENWEATHER_API_KEY = "38848f06536b1d42a209867990146039"
LINE_NOTIFY_TOKEN = "OswDEb3UcPrx085fL73uE6hOonmSg6C8n80H9fC9sA5"

@app.route('/')
def index():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # 広島の座標が届いているかチェック
    if lat and "34." in lat:
        city = "東広島市付近"
        pop = 0 # APIが不安定なため一旦0固定
        msg_text = "位置情報の取得に成功しました！"
    elif lat:
        city = "移動先"
        pop = 0
        msg_text = f"座標({lat})を確認しました。"
    else:
        city = "東京都（デフォルト）"
        pop = 0
        msg_text = "位置情報を許可すると東広島に切り替わります。"

    # APIからデータを取る（失敗してもエラー画面を出さない）
    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat if lat else '35.6895'}&lon={lon if lon else '139.6917'}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = requests.get(weather_url, timeout=5).json()
        if 'name' in res:
            # APIが動いていれば名前を上書き
            raw_name = res.get('name')
            if "Higashihiroshima" in raw_name: city = "東広島市"
    except:
        pass

    return render_template('index.html', city=city, pop=pop, message=msg_text)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)