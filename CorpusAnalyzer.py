import string
import spacy
import math

def guiraud_index_lemmatized(text: list) -> float:
    """
    Diese Funktion lemmatisiert den übergebenen Text, bzw. die Liste mit den Aussagen, die zuvor z. B. mit der Funktion
    get_speaches_from_politican() erstellt und/oder der mit create_cleaned_corpus() bereinigt wurde.
    Daraufhin wird der Index von Guirand (Typen-Token-Verhältnis) bestimmt, indem die Anzahl der Worttypen durch die
    Wurzel der Anzahl der Token des Texts geteilt wird.

    Args:
        text: Die Liste mit Äußerungen.
    Return:
        Der Index von Guirand als Fließkommazahl (float).
    """
    nlp = spacy.load("de_core_news_sm")
    nlp.max_length = 10000000
    text = " ".join(text)
    doc = nlp(text)
    lemmatized_words = [token.lemma_.lower() for token in doc if token.text.isalnum()]
    print(lemmatized_words)
    return len(set(lemmatized_words)) / math.sqrt(len(lemmatized_words)) if lemmatized_words else 0

def calculate_guiraud_naive(text: list) -> float:
    """
    Diese Funktion berechnet den Index von Guirand (Typen-Token-Verhältnis) für den übergebenen Text, indem die Anzahl
    der Worttypen durch die Wurzel der Anzahl der Token des Texts geteilt wird.
    Der übergebene Text sollte als Liste zuvor z. B. mit der Funktion get_speaches_from_politican() erstellt und/oder
    mit create_cleaned_corpus() bereinigt worden sein. Die Implementierung ist "naiv" im Sinne von unausgereift, da
    keine Lemmatiseriung erfolgt.

    Args:
        text: Die Liste mit Äußerungen.
    Return:
        Der Index von Guirand als Fließkommazahl (float).
    """

    tokens = "".join(text).split()

    types = set(tokens)

    ttr = len(types) / math.sqrt(len(tokens))

    return ttr

def kwic(corpus: str, keyword: str, l: int = 5, r: int = 5) -> list:
    """
    Diese Funktion gibt den Kontext eines Keywords in einem Text zurück. Standardmäßig sind dies die fünf Wörter rechts
    des Keywords und die fünf Wörter links des Keywords. Der Text sollte als String übergeben werden.

    Args:
         corpus: Das Korpus als String.
         keyword: Das Schlüsselwort, für das der Kontext bestimmt werden soll.
         l: Die linkseite Breite des Kontexts.
         r: Die rechtsseitige Breite des Kontexts.
    Return:
        Eine Liste mit allen Worten, die in den Index-Intervall [i-l, i+r] stehen,
        wobei i der/die Indizes des Schlüsselworts sind und ein Inkrement des Index das nächste Wort verweist.
    """

    context = []

    '''if type(corpus) == dict:
        for e in corpus.keys():
            root = corpus[e]
            for sp_tag in root.findall(".//sp"):
                for a in sp_tag.findall((".//p")):
                    ki = a.text.lower().index(keyword.lower())
                    if ki:
                        temp = a.text.split(" ")
                        temp = [entry.lower() for entry in temp if not entry.contains(string.punctuation)]
                        try:
                            context.append(temp[ki - l:ki])
                        except Exception:
                            context.append(temp[0:ki])
                        try:
                            context[-1].append(temp[ki:ki + r + 1])
                        except Exception:
                            context[-1].append(temp[ki:len(temp) - 1])'''
    if type(corpus) == str:
        temp = corpus.split(" ")
        temp = [entry.lower() for entry in temp if not all(char in string.punctuation for char in entry)]
        ki = temp.index(keyword.lower())
        print(temp)
        print(ki)
        if ki:
            if ki - l >= 0:
                context.append(temp[ki - l:ki])
            else:
                context.append(temp[0:ki])
            try:
                context[-1] = context[-1] + (temp[ki:ki + r + 1])
            except Exception:
                context[-1].append(temp[ki:len(temp) - 1])
    return context
