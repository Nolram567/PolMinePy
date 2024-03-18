import CorpusManager as cm
import spacy
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from nltk.corpus import stopwords
import nltk
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

def preprocess_text(text):

    # Tokenisierung und Lemmatisierung mit Spacy
    nlp.max_length = 10000000
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if token.lemma_ not in stop_words]

    cleaned_text = [word for word in lemmatized if word.isalpha()]

    return cleaned_text

if __name__ == "__main__":

    full_corpus = cm.create_partition()
    l = cm.get_speaches_from_politican(full_corpus, "Olaf Scholz")
    texts = cm.create_cleaned_corpus(l)

    #Übersetzung einzelner Reden in ein singuläres String-Objekt
    texts = [" ".join(texts)]

    print(f'Das Korpus hat den Umfang {len(" ".join(texts))}')
    nltk.download('stopwords')

    # Lemmatisierung
    nlp = spacy.load('de_core_news_sm', disable=['parser', 'ner'])

    # Lade deutsche Stoppwörter
    stop_words = stopwords.words('german')

    # Vorverarbeitung
    texts_preprocessed = [preprocess_text(text) for text in texts]
    dictionary = Dictionary(texts_preprocessed)

    # Generation des Bag-of-Words-Korpus
    corpus = [dictionary.doc2bow(text) for text in texts_preprocessed]


    # Generation des LDA-Modells
    lda_model = LdaModel(corpus=corpus,
                         id2word=dictionary,
                         num_topics=10,
                         random_state=100,
                         update_every=1,
                         chunksize=100,
                         passes=10,
                         alpha='auto',
                         per_word_topics=True)

    '''for idx, topic in lda_model.print_topics(-1):
        print('Topic: {} \nWords: {}'.format(idx, topic))'''

    # Visualisierung des LDA-Models
    vis = gensimvis.prepare(lda_model, corpus, dictionary)

    # Speichern der Visualisierung als HTML-Datei
    pyLDAvis.save_html(vis, 'lda_olaf-scholz.html')
