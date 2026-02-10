import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "Dcb2c4d8af0212f468f270bfcdc1dccf"
# あなたが取得したチャネルアクセストークン
LINE_TOKEN = "oswDEb3UcLCFberdDbl9YlJym+3i0X5RAppdK2qBGtDn8c85EpHNw/qcG+maHGUoI7E4V9BwiLX85dC7eKKCkIZjhtf2dyx6BVJmIRwfZCpxmpjHDFaBQTYVM+bb1i/Xt04cJ1RfpQ80nGlavV9/GgdB04t89/1O/w1cDnyilFU="

AREAS = {
    "higashihiroshima": {"name": "東広島市", "lat": "34.399", "lon": "132.744"},
    "hiroshima": {"name": "広島市", "lat": "34.385", "lon": "132.455"},
    "tokyo": {"name": "東京都", "lat": "35.689", "lon": "139.691"}
}

# --- LINE Messaging API で全員に送る命令 ---
def send_line_broadcast(message_text):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    payload = {
        "messages": [{"type": "text", "text": message_text}]
    }
    requests.post(url, headers=headers, json=payload)

@app.route('/')
def index():
    area_id = request.args.get('area', 'higashihiroshima')
    area = AREAS.get(area_id, AREAS['higashihiroshima'])
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={area['lat']}&lon={area['lon']}&appid={API_KEY}&units=metric&lang=ja"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            temp = round(data['list'][0]['main']['temp']) 
            pop = int(data['list'][0].get('pop', 0) * 100)
            status = "傘が必要です" if pop >= 30 else "傘は不要です"
            msg = f"気温は{temp}度です。{status}"
            
            # --- ここで実際に LINE 通知を実行 ---
            line_text = f"【RainCall】\n{area['name']}の天気をお知らせします。\n気温：{temp}度\n降水確率：{pop}%\n判定：{status}"
            send_line_broadcast(line_text)
            
            return render_template('index.html', city=area['name'], pop=pop, message=msg)
        else:
            return f"APIエラーが発生しました。"
            
    except Exception as e:
        return f"エラー: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)