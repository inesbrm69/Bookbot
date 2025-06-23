from nlp import classify_intent, extract_entities
from google_books_api import search_books, get_summary_by_title
from utils import format_books, correct_text

class BookChatbot:
    def messenger(self, user_input: str) -> str:
        corrected_input = correct_text(user_input)  # << correction ici
        intent = classify_intent(corrected_input)
        entities = extract_entities(corrected_input)
        return self.responder(intent, entities)

    def responder(self, intent: str, entities: dict) -> str:
        if intent == "book_search":
            books = search_books(entities)
            return format_books(books)
        elif intent == "book_summary":
            return get_summary_by_title(entities.get("title"))
        else:
            return "Je ne suis pas sûr de ce que tu veux dire. Essaie de demander un résumé ou un type de livre."