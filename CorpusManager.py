import string
import xml.etree.ElementTree as ET
import os
from pathlib import Path

import CorpusAnalyzer


def create_partition(lp: range or int or list,
                     s: range or int or list or float = float("inf")) -> dict:
    partition = {}
    if type(lp) == range:
        for i in lp:
            for j, entry in enumerate(Path(f"{f'0{i}' if i<10 else i}").iterdir()):
                partition[entry.name] = ET.parse(f"{f'0{i}' if i<10 else i}/{entry.name}")
                if j == s:
                    break
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

def kwic(corpus: dict or str, keyword: str, l: int= 5, r: int= 5) -> list:
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
                            context.append(temp[ki-l:ki])
                        except Exception:
                            context.append(temp[0:ki])
                        try:
                            context[-1].append(temp[ki:ki+r+1])
                        except Exception:
                            context[-1].append(temp[ki:len(temp)-1])
    if type(corpus) == str:
        temp = corpus.split(" ")
        temp = [entry.lower() for entry in temp if not all(char in string.punctuation for char in entry)]
        ki = temp.index(keyword.lower())
        print(temp)
        print(ki)
        if ki:
            if ki-l >= 0:
                context.append(temp[ki-l:ki])
            else:
                context.append(temp[0:ki])
            try:
                context[-1] = context[-1] + (temp[ki:ki + r+1])
            except Exception:
                context[-1].append(temp[ki:len(temp) - 1])
    return context

def create_lemmatized_corpus(l: list) -> list:
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

    test = create_partition(range(17, 18), 1)
    l = get_speaches_from_politican(test, "Angela Merkel")
    print(l)
    print(create_lemmatized_corpus(l))


    #print([entry for entry in ("hdafe", "chuieafg", "-", ".-)", "test") if not all(char in string.punctuation for char in entry)])
    #print(l)
    #print(kwic(l, "ich"))

