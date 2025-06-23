# google_books_api.py

import requests

def is_french(text):
    """Détecte si le texte est probablement en français."""
    common_french_words = [' le ', ' la ', ' les ', ' un ', ' une ', ' des ', ' ce ', ' cette ', ' dans ', ' pour ', ' pas ']
    text = ' ' + text.lower() + ' '
    return any(word in text for word in common_french_words)

def fetch_books_advanced(query, max_results=10, min_year=None, min_rating=None):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "maxResults": max_results,
        "printType": "books",
        "langRestrict": "fr"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException:
        return ["Erreur lors de la connexion à l'API Google Books."]

    if response.status_code != 200:
        return []

    books = response.json().get("items", [])
    results = []

    for book in books:
        info = book.get("volumeInfo", {})
        title = info.get("title", "Titre inconnu")
        authors = info.get("authors", ["Auteur inconnu"])
        description = info.get("description", "")
        rating = info.get("averageRating", None)
        published_date = info.get("publishedDate", "")

        # Exclure les livres sans description ou non francophones
        if not description or not is_french(description):
            continue

        # Vérification de l'année
        if min_year:
            try:
                year = int(published_date[:4])
                if year < min_year:
                    continue
            except:
                continue

        # Vérification de la note
        if min_rating:
            if not rating or rating < min_rating:
                continue

        # Formatage du résultat
        result = f"📘 *{title}* - {', '.join(authors)}\n"
        if rating:
            result += f"⭐ Note moyenne : {rating}/5\n"
        result += f"📝 Résumé : {description[:400].strip()}..."

        results.append(result)

        if len(results) >= 5:
            break

    return results
