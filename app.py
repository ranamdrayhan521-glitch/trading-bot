import time
import threading
import json
import urllib.request
from flask import Flask, jsonify

app = Flask(__name__)

latest_signal = {
    "pair": "BTC/USDT (Live)",
    "price": 0.0,
    "prev_price": 0.0,
    "signal": "⏳ ANALYZING MARKET...",
    "time": ""
}

def background_market_scanner():
    global latest_signal
    last_known_price = 0.0
    
    while True:
        try:
            # Binance Public API
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode())
                current_price = float(res_data['price'])
                
            # এনালাইসিস লজিক
            if last_known_price == 0.0:
                chosen_signal = "⏳ ANALYZING..."
            elif current_price > last_known_price:
                chosen_signal = "🟢 CALL (UP)"
            elif current_price < last_known_price:
                chosen_signal = "🔴 PUT (DOWN)"
            else:
                chosen_signal = "⏸️ HOLD / SIDEWAYS"
                
            last_known_price = current_price
            
            latest_signal = {
                "pair": "BTC/USDT (Live)",
                "price": current_price,
                "prev_price": last_known_price,
                "signal": chosen_signal,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"[REAL-TIME] Price: {current_price} | Signal: {chosen_signal}")
            
        except Exception as e:
            print(f"[ERROR] Live fetch failed: {e}")
            
        time.sleep(3)

# ব্যাকগ্রাউন্ড থ্রেড স্টার্ট
scanner_thread = threading.Thread(target=background_market_scanner)
scanner_thread.daemon = True
scanner_thread.start()

@app.route('/')
def home():
    return "🚀 Real-Time Trading Bot Server is Active!"

@app.route('/get-signal', methods=['GET'])
def get_signal():
    return jsonify(latest_signal)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
