import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# 取得したAPIキーをここに貼り付け
API_KEY = "dcb2c4d8af0212f468f270bfcdc1dccf"

AREAS = {
    "higashihiroshima": {"name": "東広島市", "lat": "34.399", "lon": "132.744"},
    "hiroshima": {"name": "広島市", "lat": "34.385", "lon": "132.455"},
    "tokyo": {"name": "東京都", "lat": "35.689", "lon": "139.691"}
}

@app.route('/')
def index():
    area_id = request.args.get('area', 'higashihiroshima')
    area = AREAS.get(area_id, AREAS['higashihiroshima'])
    
    # 5日間/3時間おきの予報を取得（降水確率が取れるのはこれ）
    url = url = f"https://api.openweathermap.org/data/2.5/forecast?lat={area_info['lat']}&lon={area_info['lon']}&appid={API_KEY}&units=metric&lang=ja"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
         temp = data['list'][0]['main']['temp']   
            # 最初の予報データから降水確率(pop)を取得 (0.0~1.0なので100倍)
            # APIから0.0〜1.0の数字を抜き取って、100倍して整数にする
            pop = int(res['list'][0].get('pop', 0) * 100)
            msg = "傘が必要です" if pop >= 30 else "傘は不要です"
            return render_template('index.html', city=area['name'], pop=pop, message=msg)
        else:
            # キーが有効化待ち(401)などの場合
            return render_template('index.html', city=area['name'], pop="--", message=f"API準備中 (Status: {response.status_code})")
    except:
        return render_template('index.html', city=area['name'], pop="--", message="通信エラーが発生しました")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)