import requests
from utils import is_french, clean_text

def get_summary_by_title(title: str) -> str:
    if not title:
        return "Je n’ai pas compris le titre du livre. Essaie par exemple : 'Donne-moi le résumé de *After*'."

    params = {
        "q": f"intitle:{title}",
        "maxResults": 1,
        "printType": "books",
        "langRestrict": "fr"
    }
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=params)
    if r.status_code != 200:
        return "❌ Erreur lors de la recherche du résumé."

    items = r.json().get("items", [])
    if not items:
        return f"Désolé, je n’ai trouvé aucun résumé pour « {title} »."

    info = items[0].get("volumeInfo", {})
    description = info.get("description", "")
    link = info.get("infoLink", "")
    display_title = info.get("title", title)

    if description and is_french(description):
        result = f"📝 Résumé de *{display_title}* :\n{description}"
        if link:
            result += f"\n🔗 Voir sur Google Books : {link}"
        return result
    else:
        return f"Désolé, je n’ai pas trouvé de résumé en français pour « {title} »."

def search_books(entities: dict) -> list:
    query = clean_text(entities.get("keywords", ""))
    min_year = entities.get("min_year")
    min_rating = entities.get("min_rating")

    params = {
        "q": query,
        "maxResults": 10,
        "printType": "books",
        "langRestrict": "fr"
    }

    r = requests.get("https://www.googleapis.com/books/v1/volumes", params=params)
    if r.status_code != 200:
        return ["Erreur lors de la recherche."]

    books = []
    for item in r.json().get("items", []):
        info = item.get("volumeInfo", {})
        desc = info.get("description", "")
        title = info.get("title", "Titre inconnu")
        authors = ", ".join(info.get("authors", ["Auteur inconnu"]))
        rating = info.get("averageRating", None)
        pub_date = info.get("publishedDate", "")
        link = info.get("infoLink", "")

        if not desc or not is_french(desc):
            continue

        if min_year:
            try:
                pub_year = int(pub_date[:4])
                if pub_year < min_year:
                    continue
            except:
                continue

        if min_rating and (not rating or rating < min_rating):
            continue

        out = f"📘 *{title}* - {authors}"
        if rating:
            out += f"\n⭐ Note : {rating}/5"
        out += f"\n📝 {desc[:400].strip()}..."
        if link:
            out += f"\n🔗 Voir sur Google Books : {link}"
        books.append(out)

        if len(books) >= 5:
            break

    return books