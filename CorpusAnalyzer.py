import string
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


def kwic(corpus: dict or str, keyword: str, l: int = 5, r: int = 5) -> list:
    context = []

    if type(corpus) == dict:
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
                            context[-1].append(temp[ki:len(temp) - 1])
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
