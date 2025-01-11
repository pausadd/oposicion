# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")
#nlp = spacy.load("es_core_news_sm")

# Process whole documents
text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")
#text = ("Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces una aldea de 20 casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas que se precipitaban por un lecho de piedras pulidas, blancas y enormes como huevos prehistóricos. El mundo era tan reciente, que muchas cosas carecían de nombre, y para mencionarlas había que señalarlas con el dedo")
"""text = ("Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía"
        " había de recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. "
        "Macondo era entonces una aldea de 20 casas de barro y cañabrava construidas a la orilla "
        "de un río de aguas diáfanas que se precipitaban por un lecho de piedras pulidas, blancas "
        "y enormes como huevos prehistóricos. El mundo era tan reciente, que muchas cosas carecían de "
        "nombre, y para mencionarlas había que señalarlas con el dedo")
"""
doc = nlp(text)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
