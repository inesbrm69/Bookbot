from chatbot import BookChatbot

def chat():
    print("📚 Bienvenue dans le Chatbot de suggestions de livres !")
    print("Tu peux me poser toutes sortes de questions :")
    print("- Je veux un livre sur les dragons et la guerre")
    print("- Un roman qui se passe à Paris noté au-dessus de 4")
    print("- Peux-tu me donner le résumé du livre After ?")
    print("- Je cherche un polar publié après 2015")
    print("Tape 'exit' pour quitter.\n")

    bot = BookChatbot()

    while True:
        user_input = input("🗨️  Toi : ")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("👋 À bientôt et bonne lecture !")
            break

        response = bot.messenger(user_input)
        print(f"\n🤖 Bot :\n{response}\n")

if __name__ == "__main__":
    chat()
