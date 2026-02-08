import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    # サーバーが生きているか確認するためのページ
    return "RainCall is Live!"

@app.route("/callback", methods=['POST'])
def callback():
    # LINEからの通知を受け取る窓口（今はOKと返すだけ）
    return 'OK'

if __name__ == "__main__":
    # Renderから指定されるポート番号を使って起動する設定
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)