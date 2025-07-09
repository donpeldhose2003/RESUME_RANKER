import spacy
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if token.is_alpha and token.lemma_ not in stop_words
    ]
    return " ".join(tokens)

def extract_skills(text, known_skills):
    text = text.lower()
    found_skills = [skill for skill in known_skills if skill.lower() in text]
    return found_skills
