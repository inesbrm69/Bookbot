# chatbot.py

from google_books_api import fetch_books_advanced

# Liste de genres connus + synonymes
GENRES = {
    "new romance": ["new romance", "romance moderne"],
    "dark romance": ["dark romance", "romance sombre"],
    "fantasy": ["fantasy", "fantaisie"],
    "thriller": ["thriller", "suspense"],
    "science-fiction": ["science-fiction", "sci-fi", "sf"],
    "classique": ["classique", "littérature classique"],
    "développement personnel": ["développement personnel", "coaching", "motivation"],
    "polar": ["polar", "roman policier"],
    "jeunesse": ["jeunesse", "ados", "enfants"],
    "historique": ["historique", "roman historique"]
}

def clean_text(text):
    return text.lower().strip()

def detect_genre(user_input):
    """Détecte si un genre connu est mentionné dans la requête."""
    text = clean_text(user_input)
    for genre, keywords in GENRES.items():
        if any(k in text for k in keywords):
            return genre
    return None

def extract_filters(user_input):
    """
    Analyse la requête pour en extraire :
    - Les mots-clés (entiers si pas de genre)
    - Une année minimale ("après 2015", "depuis 2020")
    - Une note minimale ("note de 4", "noté au-dessus de 3.5")
    """
    filters = {
        "keywords": user_input,
        "min_year": None,
        "min_rating": None
    }

    text = clean_text(user_input)

    # Recherche d'année (ex: "après 2015", "depuis 2020")
    for word in text.split():
        if word.isdigit() and 1900 < int(word) < 2100:
            filters["min_year"] = int(word)
            break

    # Recherche de note minimale (ex: "note de 4", "noté au-dessus de 3.5")
    for word in text.replace(",", ".").split():
        try:
            note = float(word)
            if 0 < note <= 5:
                filters["min_rating"] = note
                break
        except:
            continue

    return filters

def generate_response(user_input):
    genre = detect_genre(user_input)
    filters = extract_filters(user_input)

    if genre:
        filters["keywords"] = genre  # Remplace les mots-clés par le genre détecté

    suggestions = fetch_books_advanced(
        query=filters["keywords"],
        min_year=filters["min_year"],
        min_rating=filters["min_rating"]
    )

    if suggestions:
        return "📚 Voici quelques livres correspondant à ta recherche :\n\n" + "\n\n".join(suggestions)
    else:
        return "😕 Je n’ai pas trouvé de livres correspondant à ta demande. Essaie de reformuler ou choisis un autre thème."