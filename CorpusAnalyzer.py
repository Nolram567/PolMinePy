import spacy

def guiraud_index_lemmatized(text: list):
    nlp = spacy.load("de_core_news_sm")
    nlp.max_length = 10000000
    text = " ".join(text)
    doc = nlp(text)
    lemmatized_words = [token.lemma_.lower() for token in doc if token.text.isalnum()]
    print(lemmatized_words)
    return len(set(lemmatized_words)) / len(lemmatized_words) if lemmatized_words else 0

def calculate_guiraud_naive(text: list):

    tokens = "".join(text).split()

    types = set(tokens)

    ttr = len(types) / len(tokens)

    return ttr
