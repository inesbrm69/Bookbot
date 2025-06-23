import difflib

KNOWN_WORDS = [
    "livre", "roman", "résumé", "guerre", "seconde", "auteur", "note", "année",
    "thriller", "polar", "fantasy", "new romance", "dark romance", "historique", "science-fiction",
    "je veux", "je cherche", "histoire", "parle", "monde", "après", "avec", "résumer"
]

def correct_text(text):
    words = text.lower().split()
    corrected = []
    for word in words:
        match = difflib.get_close_matches(word, KNOWN_WORDS, n=1, cutoff=0.75)
        corrected.append(match[0] if match else word)
    return " ".join(corrected)

def is_french(text):
    common_words = [' le ', ' la ', ' les ', ' une ', ' des ', ' pour ', ' avec ']
    text = ' ' + text.lower() + ' '
    return any(w in text for w in common_words)

def clean_text(text):
    return text.lower().strip()

def format_books(books):
    return "\n\n".join(books[:5]) if books else "Aucun résultat trouvé."
