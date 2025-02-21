import spacy
import nltk
from nltk.corpus import wordnet
from known_classes import KNOWN_CLASSES  # Import the list of known classes

# Download WordNet data (run this only once)
nltk.download('wordnet')

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

def get_synonyms(word):
    """
    Get synonyms for a given word using WordNet.
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace("_", " "))  # Replace underscores with spaces
    return list(synonyms)

def extract_object_from_message(message):
    """
    Extract the object from the user's message using automated synonym detection.
    """
    doc = nlp(message)
    for token in doc:
        if token.pos_ == "NOUN":  # Look for nouns
            object_name = token.text.lower()  # Normalize to lowercase

            # Step 1: Find synonyms for the extracted noun
            synonyms = get_synonyms(object_name)

            # Step 2: Check if the original word or any synonym matches a known class
            if object_name in KNOWN_CLASSES:
                return object_name
            for synonym in synonyms:
                if synonym in KNOWN_CLASSES:
                    return synonym

            # Step 3: Return the original word if no match is found
            return object_name
    return None