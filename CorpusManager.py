import xml.etree.ElementTree as ET
import os
from pathlib import Path

def create_partition(lp: range or int or list,
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

def get_speaches_from_politican(corpus: dict, p: str, id: str = "name") -> list:
    speaches = []
    for e in corpus.keys():
        root = corpus[e]
        for sp_tag in root.findall(f".//sp[@{id}='{p}']"):
            for a in sp_tag.findall((".//p")):
                speaches.append(a.text)
    return speaches

def get_speaches_from_party(corpus: dict, p: str) -> list:
    speaches = []
    for e in corpus.keys():
        root = corpus[e]
        for sp_tag in root.findall(f".//sp[@party='{p}']"):
            for a in sp_tag.findall((".//p")):
                speaches.append(a.text)
    return speaches

if __name__ == "__main__":

    test = create_partition(range(17, 19))
    l = get_speaches_from_party(test, "CDU")
    print(l[1:12])

