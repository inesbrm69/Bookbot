from chatbot import BookChatbot
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/chat', methods=['POST'])
def chat():
    """
    print("📚 Bienvenue dans le Chatbot de suggestions de livres !")
    print("Tu peux me poser toutes sortes de questions :")
    print("- Je veux un livre sur les dragons et la guerre")
    print("- Un roman qui se passe à Paris noté au-dessus de 4")
    print("- Peux-tu me donner le résumé du livre After ?")
    print("- Je cherche un polar publié après 2015")
    print("Tape 'exit' pour quitter.\n")
"""
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': "Missing 'message' in JSON body"}), 400

    bot = BookChatbot()

    user_input = data['message']
    response = bot.messenger(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
