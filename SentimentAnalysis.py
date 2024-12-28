import CorpusManager
from germansentiment import SentimentModel


def calculate_polarity(p: list) -> float:
    """
    Diese Funktion nutzt GBERT, um die Sentiment-Polarität für eine Liste von Strings (wie Absätze oder Sätze) zu berechnen.
    Sie teilt die Liste `p` in Unterlisten von maximal 100 Einträgen auf, berechnet die Sentiments für jede Unterliste
    und kombiniert die Ergebnisse. Diese Unterteilung der Liste ist notwendig, da es bei einigen Rechnern, abhängig von
    der Hardware, nicht genügend Hauptspeicher vorhanden ist.

    Args:
        p: Liste von Textabschnitten.
    Return:
        Die durchschnittliche Polarität als float.
    """
    model = SentimentModel()

    ''' Aufteilung der Absatz-Liste in chunks, da es aber ~1000 Einträgen zu einem Memory-Overflow kommt. Die chunks
     werden separat berechnet.'''
    chunk_size = 100
    chunks = [p[i:i + chunk_size] for i in range(0, len(p), chunk_size)]

    total_polarity = 0

    # Berechnung der Polarität für jeden Chunk
    for chunk in chunks:
        chunk_result = model.predict_sentiment(chunk)

        # Berechnung der Polarität für den aktuellen Chunk
        for s in chunk_result:
            if s == 'neutral':
                continue
            elif s == 'negative':
                total_polarity -= 1
            else:
                total_polarity += 1

    # Berechnung der durchschnittlichen Polarität über alle Einträge
    return total_polarity / len(p) if p else 0

def filter_topic(corpus: list, t: list) -> list:
    """
    Diese Funktion filtert die Liste corpus, indem sie alle Einträge entfernt, die keinen String aus t enthalten.

    Args:
         corpus: Die Liste mit Strings, die gefiltert werden soll.
         t: Die Liste mit Strings mit denen gefiltert werden soll.
    Return:
        Die gefilterte Liste.
    """
    return [text for text in corpus if any(term in text for term in t)]


if __name__ == '__main__':


        '''
        Wir laden die Legislaturperioden: 
        '''
        LP17 = CorpusManager.create_partition(17)
        LP18 = CorpusManager.create_partition(18)
        LP19 = CorpusManager.create_partition(19)


        '''Die Definition der Themenlexika:'''

        Topic_climate = ["klima", "umwelt", "emission", "erneuerbare energie", "nachhaltigkeit", "energiewende",
                         "greenwashing", "kohleausstieg", "biodiversitätsverlust", "öko-diktatur",
                         "fossile brennstoffe", "klimaflüchtlinge"]

        Topic_migration = ["asylbewerber", "multikulturalismus", "flüchtlingskrise", "grenzkontrolle",
                           "willkommenskultur", "wirtschaftsmigranten", "abschiebung", "duldung", "einwanderungsgesetz",
                           "familiennachzug", "integration", "ankerzentren", "fremdenfeindlichkeit", "bleiberecht",
                           "asylverfahren", "residenzpflicht", "arbeitsmigration", "visapolitik", "migration"]

        Topic_democracy = ["demokratie", "grundgesetz", "gewaltenteilung", "pluralismus", "bundestag", "parteiensystem",
                           "meinungsfreiheit", "zivilgesellschaft", "rechtsstaatlichkeit", "volksabstimmung",
                           "parlamentarismus"]

        '''
        Wir tokenisieren die Absätze unserer Korpora. Und normalisieren nach Kleinschreibung.
        '''

        LP19_p = CorpusManager.tokenize_paragraphs(LP19)
        LP18_p = CorpusManager.tokenize_paragraphs(LP18)
        LP17_p = CorpusManager.tokenize_paragraphs(LP17)

        LP19_p = CorpusManager.normalize_case(LP19_p)
        LP18_p = CorpusManager.normalize_case(LP18_p)
        LP17_p = CorpusManager.normalize_case(LP17_p)

        '''
        Wir filtern die Absätze nach Themen:
        '''

        LP19_p_climate = filter_topic(LP19_p, Topic_climate)
        LP19_p_migration = filter_topic(LP19_p, Topic_migration)
        LP19_p_democracy = filter_topic(LP19_p, Topic_democracy)

        LP18_p_climate = filter_topic(LP18_p, Topic_climate)
        LP18_p_migration = filter_topic(LP18_p, Topic_migration)
        LP18_p_democracy = filter_topic(LP18_p, Topic_democracy)

        LP17_p_climate = filter_topic(LP17_p, Topic_climate)
        LP17_p_migration = filter_topic(LP17_p, Topic_migration)
        LP17_p_democracy = filter_topic(LP17_p, Topic_democracy)

        '''Wir berechnen die Polarität der Themen:'''

        LP19_p_climate_polarity = calculate_polarity(LP19_p_climate)
        LP19_p_migration_polarity = calculate_polarity(LP19_p_migration)
        LP19_p_democracy_polarity = calculate_polarity(LP19_p_democracy)

        LP18_p_climate_polarity = calculate_polarity(LP18_p_climate)
        LP18_p_migration_polarity = calculate_polarity(LP18_p_migration)
        LP18_p_democracy_polarity = calculate_polarity(LP18_p_democracy)

        LP17_p_climate_polarity = calculate_polarity(LP17_p_climate)
        LP17_p_migration_polarity = calculate_polarity(LP17_p_migration)
        LP17_p_democracy_polarity = calculate_polarity(LP17_p_democracy)

        '''Wir drucken die Ergebnisse: '''

        print(f"Die mittlere Polarität des Themas 'Klima' beträgt in den Legislaturperioden 17, 18 und 19:"
              f" {LP17_p_climate_polarity}, {LP18_p_climate_polarity} und {LP19_p_climate_polarity}")

        print(f"Die mittlere Polarität des Themas 'Migration' beträgt in den Legislaturperioden 17, 18 und 19:"
              f" {LP17_p_migration_polarity}, {LP18_p_migration_polarity} und {LP19_p_migration_polarity}")

        print(f"Die mittlere Polarität des Themas 'Demokratie' beträgt in den Legislaturperioden 17, 18 und 19:"
              f" {LP17_p_democracy_polarity}, {LP18_p_democracy_polarity} und {LP19_p_democracy_polarity}")

        '''
        Die mittlere Polarität des Themas 'Klima' beträgt in den Legislaturperioden 17, 18 und 19: -0.059932125063181456, -0.06584121141136116 und -0.09851177923721155
        Die mittlere Polarität des Themas 'Migration' beträgt in den Legislaturperioden 17, 18 und 19: -0.07823199833990455, -0.06559810032650638 und -0.102303645927807
        Die mittlere Polarität des Themas 'Demokratie' beträgt in den Legislaturperioden 17, 18 und 19: -0.0918372307841898, -0.07395362842517314 und -0.11040949100650593
        '''

        '''
        Wir führen dieselbe Prozedur noch einmal für alle Redebeiträge der AfD während der 19. Legislaturperiode durch:
        '''

        LP19_AfD = CorpusManager.get_speaches_from_party(LP19, 'AfD')

        LP19_AfD_climate = filter_topic(LP19_AfD, Topic_climate)
        LP19_AfD_migration = filter_topic(LP19_AfD, Topic_migration)
        LP19_AfD_democracy = filter_topic(LP19_AfD, Topic_democracy)

        LP19_AfD_climate = CorpusManager.normalize_case(LP19_AfD_climate)
        LP19_AfD_migration = CorpusManager.normalize_case(LP19_AfD_migration)
        LP19_AfD_democracy = CorpusManager.normalize_case(LP19_AfD_democracy)

        LP19_AfD_climate_s = calculate_polarity(LP19_AfD_climate)
        LP19_AfD_migration_s = calculate_polarity(LP19_AfD_migration)
        LP19_AfD_democracy_s = calculate_polarity(LP19_AfD_democracy)

        '''
        Die mittlere Polarität des Themas 'Klima' beträgt für die AfD in der 19. Legislaturperiode:-0.09905660377358491.
        Die mittlere Polarität des Themas 'Migration' beträgt für die AfD in der 19. Legislaturperiode: -0.11382113821138211.
        Die mittlere Polarität des Themas 'Demokratie' beträgt für die AfD in der 19. Legislaturperiode: -0.1640625.
        '''
