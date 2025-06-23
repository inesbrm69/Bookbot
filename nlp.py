import re

def classify_intent(text: str) -> str:
    text = text.lower()
    if "résumé" in text or "resume" in text:
        return "book_summary"
    keywords = ["livre", "roman", "lire", "auteur", "note", "thème", "genre", "histoire"]
    if any(word in text for word in keywords):
        return "book_search"
    return "unknown"

# Requête : "Je veux un livre triste" → transformé en drame, "Résumé de Dune" → extrait le titre, "Un thriller après 2015 noté au-dessus de 4" → extrait tous les filtres
def extract_entities(text: str) -> dict:
    text = text.lower().strip()

    # Ambiance → genre
    emotion_map = {
        "triste": "drame",
        "drôle": "comédie",
        "effrayant": "thriller",
        "romantique": "romance",
        "relaxant": "feel-good",
        "mystérieux": "polar",
        "intense": "dark romance"
    }

    # On initialise le genre par défaut avec le texte complet
    keywords = text
    for word, genre in emotion_map.items():
        if word in text:
            keywords = genre  # on remplace par le genre correspondant
            break  # on prend le premier mot reconnu

    # Initialisation de l'objet entité
    entities = {
        "keywords": keywords,
        "min_year": None,
        "min_rating": None,
        "title": None
    }

    # Titre entre guillemets
    match = re.search(r'["“”«](.+?)["”»]', text)
    if match:
        entities["title"] = match.group(1)

    # Titre après "résumé de ..."
    if "résumé de" in text:
        after = text.split("résumé de")[-1].strip()
        entities["title"] = after.strip(' "\'?.')

    # Année après ou depuis
    match = re.search(r"(après|depuis)\s*(\d{4})", text)
    if match:
        entities["min_year"] = int(match.group(2))

    # Note (ex: "note de 4", "noté au-dessus de 3,5")
    match = re.search(r"(note|noté|notes).*?(\d(?:[.,]\d)?)", text)
    if match:
        entities["min_rating"] = float(match.group(2).replace(",", "."))

    return entities
