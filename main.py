from chatbot import generate_response

def chat():
    print("📚 Bienvenue dans le Chatbot de suggestions de livres via Google Books !")
    print("Pose-moi une question comme :")
    print("- 'Je veux lire une dark romance'")
    print("- 'Tu as un livre sur les dragons et la guerre ?'")
    print("- 'Un thriller après 2015 avec une bonne note'")
    print("- 'As-tu un roman qui se passe à Paris ?'")
    print("Tape 'exit' pour quitter.\n")

    while True:
        user_input = input("🗨️  Toi : ")
        if user_input.lower().strip() in ["exit", "quit", "bye"]:
            print("👋 À bientôt et bonne lecture !")
            break
        response = generate_response(user_input)
        print(f"\n🤖 Bot :\n{response}\n")

if __name__ == "__main__":
    chat()
