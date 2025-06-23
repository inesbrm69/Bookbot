from nlp import classify_intent, extract_entities
from google_books_api import search_books, get_summary_by_title
from utils import format_books, correct_text

class BookChatbot:
    def __init__(self):
        self.last_entities = None  # mémoire de la dernière demande

    def messenger(self, user_input: str) -> str:
        corrected_input = correct_text(user_input).strip().lower()

        # Requête de relance basée sur la mémoire
        if any(phrase in corrected_input for phrase in ["un autre", "encore", "autre suggestion", "montre moi", "encore un", "dans le même style"]):
            if self.last_entities:
                import random
                offset = random.choice([5, 10, 15, 20])
                books = search_books(self.last_entities, offset=offset)
                return format_books(books)
            else:
                return "Je n’ai pas encore de recherche précédente en mémoire. Commence par me dire ce que tu veux lire 😊"

        # Traitement normal
        intent = classify_intent(corrected_input)
        entities = extract_entities(corrected_input)

        # On mémorise les entités pour relance future
        if intent in ["book_search", "random_book"]:
            self.last_entities = entities

        return self.responder(intent, entities)


    def responder(self, intent: str, entities: dict) -> str:
        if intent == "book_search":
            books = search_books(entities)
            return format_books(books)
        elif intent == "book_summary":
            return get_summary_by_title(entities.get("title"))
        elif intent == "random_book":
            from random import choice
            from random import randint
            genres = ["thriller", "fantasy", "polar", "romance", "dark romance", "science-fiction"]
            random_entities = {
                "keywords": choice(genres),
                "min_year": randint(2000, 2025),
                "min_rating": round(randint(35, 48) / 10, 1)
            }
            self.last_entities = random_entities
            return format_books(search_books(random_entities))
        else:
            return "Je ne suis pas sûr de ce que tu veux dire. Essaie de demander un résumé ou un type de livre."
