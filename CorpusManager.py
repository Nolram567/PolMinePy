import string
import xml.etree.ElementTree as ET
import os
from pathlib import Path
import matplotlib.pyplot as plt
import CorpusAnalyzer

def create_partition(lp: range or int or list = range(1, 20),
                     s: range or int or list or float = float("inf")) -> dict:
    """
    Diese Funktion lädt entweder eine Partition des GermaParl-Korpus oder das gesamte Korpus, wenn keine Argumente
    übergeben werden.

    Args:
        lp: Die Legislaturperiode(n). Die gewünschten Legislaturperioden können entweder als Intervall (range-Objekt),
        als natürliche Zahl (int) oder als Liste (list) übergeben werden. Wird kein Argument übergeben, werden alle
        Legislaturperioden geladen.
        s: Die gewünschten Sitzungen können entweder als Intervall (range-Objekt), als natürliche Zahl (int) oder
        als Liste (list) übergeben werden. Wird kein Argument übergeben, werden alle Sitzugen geladen.

    Returns:
        Die spezifizierten Legislaturperioden und Sitzungen werden in einem Dictionary zurückgegeben. Der Schlüssel ist
        immer der Dateiname nach dem Schema: BT_{Legislaturperiode}_{Sitzung} und die Werte jeweils der XML Element Tree.
    """

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
    """
    Diese Methode soll bereits erstellte Partitionen abspeichern, sodass man zwischen Sitzungen die Partition nicht
    neu erstellen muss.
    """
    pass

def get_speaches_from_politican(corpus: dict, p: str, id: str = "name", aslist: bool = True) -> list:
    """
    Mit dieser Funktion kann man alle Reden einer spezifizierten Person aus einem Korpus extrahieren. Das Korpus sollte
    zuvor mit der Funktion create_partition() erstellt wurden sein oder konform zur Struktur des Rückgabe-Dictionaries sein.

    Args:
         corpus: Das Korpus oder die Partition.
         p: Der Name der Person.
         id: Das Attribut des sp-Tags, in dem nach dem Namen (Parameter p) gesucht werden soll. Das Standardattribut ist "name".
         aslist: Hier kann der Rückgabedatentyp modifiziert werden. Der Standardwert ist eine Liste. (Die Alternativen sind
         noch nicht implementiert.)
    Return:
        Eine Liste mit allen Einzeläußerungen der spezifizierten Person ohne Metadaten.
    """
    speaches = []
    for e in corpus.keys():
        root = corpus[e]
        for sp_tag in root.findall(f".//sp[@{id}='{p}']"):
            for a in sp_tag.findall((".//p")):
                speaches.append(a.text)
    return speaches if aslist else " ".join(speaches)

def get_speaches_from_party(corpus: dict, party: str) -> list:
    """
    Mit dieser Funktion kann man alle Reden einer spezifizierten Partei aus einem Korpus extrahieren. Das Korpus sollte
    zuvor mit der Funktion create_partition() erstellt wurden sein oder konform zur Struktur des Rückgabe-Dictionaries sein.

    Args:
        corpus: Das Korpus oder die Partition.
        party: Der Name der Partei.
    Return:
        Eine Liste mit allen Einzeläußerungen von Mitglieder der spezifizierten Partei ohne Metadaten.
    """
    speaches = []
    for e in corpus.keys():
        root = corpus[e]
        for sp_tag in root.findall(f".//sp[@party='{party}']"):
            for a in sp_tag.findall((".//p")):
                speaches.append(a.text)
    return speaches
def create_cleaned_corpus(l: list) -> list:
    """
    Befreit eine Liste mit Strings, die zuvor z. B. mit get_speaches_from_party() oder get_speaches_from_politican()
    erstellt wurde, von Interpunktionszeichen.

    Args:
        l: Die zu bereinigende Liste.

    Returns:
        Die von Interpunktionszeichen befreite Liste.
    """
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

    full_corpus = create_partition(range(1,2))
    print(full_corpus)



    '''bundeskanzler_liste = [
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
'''
    #print([entry for entry in ("hdafe", "chuieafg", "-", ".-)", "test") if not all(char in string.punctuation for char in entry)])
    #test = get_speaches_from_politican(full_corpus, "Konrad Adenauer")
    print(CorpusAnalyzer.kwic(" ".join(get_speaches_from_politican(full_corpus, "Konrad Adenauer")), keyword="Problem"))
    '''
    # Sortieren des Dictionaries nach Werten in absteigender Reihenfolge
    sorted_data = dict(sorted(bk_ttr.items(), key=lambda item: item[1], reverse=True))

    plt.figure(figsize=(10, 6))
    plt.bar(sorted_data.keys(), sorted_data.values(), color='skyblue')
    plt.xlabel('Bundeskanzler')
    plt.ylabel('TTR')
    plt.title('TTR der Bundeskanzler')
    plt.xticks(rotation=45)
    #plt.savefig("TTR_bundeskanzler")
    plt.show()'''
