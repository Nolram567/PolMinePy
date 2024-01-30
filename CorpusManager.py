import xml.etree.ElementTree as ET
import os
from pathlib import Path

def create_partition(lp: range or int or list, s: range or int or list) -> dict:
    partition = {}
    for i in lp:
        for j, entry in enumerate(Path(f"0{i}").iterdir()):
            if j == s:
                break
            partition[entry.name] = ET.parse(f"0{i}/{entry.name}")
    return partition



if __name__ == "__main__":

    test = create_partition(range(1, 2), 10)
    print(test)
    for e in test.keys():
        root = test[e]
        for sp_tag in root.findall(".//sp[@who='Adenauer']"):
            who = sp_tag.get("who")
            party = sp_tag.get("party")
            name = sp_tag.get("name")
            for a in sp_tag.findall((".//p")):
                print(a.text)
            #print(f"Speaker: {name}, Party: {party}, ID: {who}")

