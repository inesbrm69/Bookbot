from chatbot import BookChatbot
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)
@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': "Missing 'message' in JSON body"}), 400

    bot = BookChatbot()

    user_input = data['message']
    response = bot.messenger(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host='0.0.0.0', port=port)
