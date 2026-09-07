import time
import random
from flask import Flask, jsonify

app = Flask(__name__)

latest_signal = {
    "pair": "BTC/USDT (Live)",
    "price": 0.0,
    "signal": "⏳ WAITING...",
    "time": ""
}

def background_market_scanner():
    global latest_signal
    while True:
        try:
            import urllib.request
            import json
            
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                current_price = float(data['price'])
            
            signals_list = ["🟢 CALL (UP)", "🔴 PUT (DOWN)", "⏳ HOLD / NO TRADE"]
            chosen_signal = random.choice(signals_list)
            
            latest_signal = {
                "pair": "BTC/USDT",
                "price": current_price,
                "signal": chosen_signal,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"[SYNC] Price: {current_price} | Signal: {chosen_signal}")
            
        except Exception as e:
            print(f"[ERROR] Fetching live data: {e}")
            
        time.sleep(3)

@app.route('/')
def home():
    return "🚀 Trading Bot Server is Alive and Running Perfectly!"

@app.route('/get-signal', methods=['GET'])
def get_signal():
    return jsonify(latest_signal)

if __name__ == '__main__':
    import threading
    t = threading.Thread(target=background_market_scanner)
    t.daemon = True
    t.start()
    
    app.run(host='0.0.0.0', port=5000)
