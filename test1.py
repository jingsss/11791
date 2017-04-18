import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp(u'I like to learn English. The price of London is  50 us dollar. The first city in the United Kingdom. I am her mother.')
for ent in doc.ents:
    print(ent.label_, ent.text)
    # GPE London
    # GPE United Kingdom


doc = nlp(u'London is a big city in the United Kingdom.')
print(doc[0].text, doc[0].ent_iob, doc[0].ent_type_)
# (u'London', 2, u'GPE')
print(doc[1].text, doc[1].ent_iob, doc[1].ent_type_)
# (u'is', 3, u'')
