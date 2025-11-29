from flask import Flask, request
import datetime
import os

app = Flask(__name__)

# کلید امنیتی - این را در TradingView هم استفاده کنید
WEBHOOK_TOKEN = "YourSecretToken123"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # بررسی توکن امنیتی
        token = request.args.get('token')
        if token != WEBHOOK_TOKEN:
            return 'Invalid Token', 401
        
        # دریافت داده از TradingView
        data = request.get_json()
        
        if data:
            # پردازش داده
            symbol = data.get('symbol', '')
            action = data.get('action', '')
            price = data.get('price', '')
            
            # ذخیره سیگنال در فایل
            signal_data = f"{symbol},{action},{price}\n"
            
            with open('signals.txt', 'w') as f:
                f.write(signal_data)
            
            print(f"✅ Signal received: {symbol} | {action} | {price}")
            return 'Signal received successfully', 200
        else:
            # اگر داده JSON نبود، به عنوان متن ساده پردازش کن
            data_text = request.get_data(as_text=True)
            if data_text:
                with open('signals.txt', 'w') as f:
                    f.write(data_text)
                print(f"✅ Text signal received: {data_text}")
                return 'Text signal received', 200
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 'Error', 500

@app.route('/signals.txt', methods=['GET'])
def get_signals():
    try:
        with open('signals.txt', 'r') as f:
            content = f.read()
        return content, 200
    except:
        return 'No signals yet', 404

@app.route('/health', methods=['GET'])
def health_check():
    return 'Server is running', 200

@app.route('/')
def home():
    return 'Trading Webhook Server is Running!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
