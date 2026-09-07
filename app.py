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
    # প্রথমে আগের প্রাইস স্টোর করার ভেরিয়েবল
    last_known_price = 0.0
    
    while True:
        try:
            # CoinCap রিয়েল-টাইম বিটকয়েন এপিআই
            url = "https://api.coincap.io/v2/assets/bitcoin"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode())
                current_price = float(res_data['data']['priceUsd'])
            
            # রিয়েল-টাইম প্রাইস অ্যাকশন এনালাইসিস লজিক
            if last_known_price == 0.0:
                chosen_signal = "⏳ ANALYZING..."
            elif current_price > last_known_price:
                chosen_signal = "🟢 CALL (UP)"  # মার্কেট উপরে উঠছে
            elif current_price < last_known_price:
                chosen_signal = "🔴 PUT (DOWN)" # মার্কেট নিচে নামছে
            else:
                chosen_signal = "⏳ HOLD / SIDEWAYS"
                
            last_known_price = current_price
            
            latest_signal = {
                "pair": "BTC/USDT (Live)",
                "price": current_price,
                "signal": chosen_signal,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"[REAL-TIME] Price: {current_price} | Signal: {chosen_signal}")
            
        except Exception as e:
            print(f"[ERROR] Live fetch failed: {e}")
            
        time.sleep(3)

# ব্যাকগ্রাউন্ড রিয়েল-টাইম থ্রেড স্টার্ট
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
            
