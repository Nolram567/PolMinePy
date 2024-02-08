import string
import xml.etree.ElementTree as ET
import os
from pathlib import Path
import matplotlib.pyplot as plt
import CorpusAnalyzer


def create_partition(lp: range or int or list = range(1, 20),
                     s: range or int or list or float = float("inf")) -> dict:
    partition = {}
    if type(lp) == range:
        for i in lp:
            for j, entry in enumerate(Path(f"{f'0{i}' if i<10 else i}").iterdir()):
                if j == s:
                    break
                partition[entry.name] = ET.parse(f"{f'0{i}' if i<10 else i}/{entry.name}")
    elif type(lp) == list:
        pass
    else:
        for j, entry in enumerate(Path(f"{f'0{lp}' if lp < 10 else lp}").iterdir()):
            if j == s:
                break
            partition[entry.name] = ET.parse(f"{f'0{lp}' if lp < 10 else lp}/{entry.name}")

    return partition

def save_partition():
    pass

def get_speaches_from_politican(corpus: dict, p: str, id: str = "name", aslist: bool = True) -> list:
    speaches = []
    for e in corpus.keys():
        root = corpus[e]
        for sp_tag in root.findall(f".//sp[@{id}='{p}']"):
            for a in sp_tag.findall((".//p")):
                speaches.append(a.text)
    return speaches if aslist else " ".join(speaches)

def get_speaches_from_party(corpus: dict, party: str) -> list:
    speaches = []
    for e in corpus.keys():
        root = corpus[e]
        for sp_tag in root.findall(f".//sp[@party='{party}']"):
            for a in sp_tag.findall((".//p")):
                speaches.append(a.text)
    return speaches
def create_cleaned_corpus(l: list) -> list:
    lc = []
    for entry in l:
        lc = lc + entry.split(" ")
    lc = [entry.lower() for entry in l if not all(char in string.punctuation for char in entry)]
    translator = str.maketrans('', '', string.punctuation)
    for i, entry in enumerate(lc):
        if any(char in string.punctuation for char in entry):
           lc[i]= entry.translate(translator)
    return lc

if __name__ == "__main__":

    full_corpus = create_partition()



    bundeskanzler_liste = [
        "Konrad Adenauer",
        "Ludwig Erhard",
        "Kurt Georg Kiesinger",
        "Willy Brandt",
        "Helmut Schmidt",
        "Helmut Kohl",
        "Gerhard Schröder",
        "Angela Merkel",
        "Olaf Scholz"
    ]

    bk_ttr = {}

    for e in bundeskanzler_liste:
        l = get_speaches_from_politican(full_corpus, e)
        am = create_cleaned_corpus(l)
        bk_ttr[e] = CorpusAnalyzer.guiraud_index_lemmatized(l)

    #print([entry for entry in ("hdafe", "chuieafg", "-", ".-)", "test") if not all(char in string.punctuation for char in entry)])
    #print(l)
    #print(kwic(l, "ich"))


    # Sortieren des Dictionaries nach Werten in absteigender Reihenfolge
    sorted_data = dict(sorted(bk_ttr.items(), key=lambda item: item[1], reverse=True))

    # Erstellen des Histogramms
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_data.keys(), sorted_data.values(), color='skyblue')
    plt.xlabel('Bundeskanzler')
    plt.ylabel('TTR')
    plt.title('TTR der Bundeskanzler')
    plt.xticks(rotation=45)  # Dreht die X-Achsen-Beschriftungen, falls sie zu lang sind
    plt.savefig("TTR_bundeskanzler")
    plt.show()
