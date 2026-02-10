import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# 提供いただいたキーをセットしました
API_KEY = "Dcb2c4d8af0212f468f270bfcdc1dccf"

AREAS = {
    "higashihiroshima": {"name": "東広島市", "lat": "34.399", "lon": "132.744"},
    "hiroshima": {"name": "広島市", "lat": "34.385", "lon": "132.455"},
    "tokyo": {"name": "東京都", "lat": "35.689", "lon": "139.691"}
}

@app.route('/')
def index():
    area_id = request.args.get('area', 'higashihiroshima')
    # 変数名を 'area' に統一（ズレを防止）
    area = AREAS.get(area_id, AREAS['higashihiroshima'])
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={area['lat']}&lon={area['lon']}&appid={API_KEY}&units=metric&lang=ja"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            # 天気予報データから気温と降水確率を抽出
            temp = data['list'][0]['main']['temp']
            pop = int(data['list'][0].get('pop', 0) * 100)
            
            msg = f"気温は{temp}度です。"
            msg += "傘が必要です" if pop >= 30 else "傘は不要です"
            
            return render_template('index.html', city=area['name'], pop=pop, message=msg)
        else:
            # キーの有効化待ちなどのエラー表示
            return f"APIエラー: {data.get('message', '不明なエラー')} (Status: {response.status_code})"
            
    except Exception as e:
        # 万が一の通信エラー用
        return f"システムエラーが発生しました: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)