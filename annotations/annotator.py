# 11-791 Annotations using the  NLTK Library 
import nltk 
from nltk import word_tokenize
from nltk.tag.stanford import StanfordNERTagger
 
import unicodedata


classifier = '/Users/ekeni/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz'
jar = '/Users/ekeni/stanford-ner/stanford-ner.jar'
st = StanfordNERTagger(classifier,jar)
# 

# Tokenizes and returns pos tags for each token
# function call 
# pos_tags("The house is painted blue")

# output 
# List if tuples
# [('The', 'DT'), ('house', 'NN'), ('is', 'VBZ'), ('painted', 'VBN'), ('blue', 'JJ')] 


def tokenize(sent):
    text = nltk.word_tokenize(sent)
    return text

def pos_tags(text):
    #text =  tokenize(sent)
    text2 = nltk.pos_tag(text)
    return text2


def named_ent1(sent):
    tagged = pos_tags(sent)
    namedEnt = nltk.ne_chunk(tagged)
    #print namedEnt
    #namedEnt.draw()
    return namedEnt

def named_ent2(sent):
    tagged = tokenize(sent)
    namedEnt = st.tag(tagged)
    #print namedEnt
    #namedEnt.draw()
    return namedEnt

def norms(k):
    for x in k:
        x[1].encode('ascii','ignore')
    return k

# using Stnaford NER Tagger 7 class 
# check for organizations 
def get_entity(k2, ent):
    l = []
    for x in k2:
        if x[1] == ent:
            # print x[0]
            l.append(x[0].encode('ascii','ignore'))
    return l



def all_entity(k2):

    l_org = get_entity(k2,"ORGANIZATION")
    l_date = get_entity(k2,"DATE")
    l_person= get_entity(k2,"PERSON")
    l_loc = get_entity(k2,"LOCATION")
    l_percent = get_entity(k2,"PERCENT")
    l_time = get_entity(k2,"TIME")
    return l_org, l_date, l_person, l_loc, l_percent, l_time


def hasNumbers(k):
    l = []
    for inputString in k:
        t = any(char.isdigit() for char in inputString)
        #print 
        l.append(t)

    return l

S ="Jack studies at Stony Brook University in New York since 1999 with 90% percentile at 5:00 pm in the evening "

# main function 
#tokenize, POS tags, is num , NER Tags
def create_annotations(sentence):

    final_ans = {}
    tokens = tokenize(S)
    k2 = named_ent2(sentence)
    final_ans['tokens'] = tokens
    final_ans['pos'] = pos_tags(tokens)
    l_org, l_date, l_person, l_loc, l_percent, l_time = all_entity(k2)
    final_ans['is_num'] = hasNumbers(k2)
    final_ans['ORG'] = l_org
    final_ans['PERSON'] = l_person
    final_ans['DATE'] = l_date
    final_ans['LOCATION'] = l_loc
    final_ans['TIME'] = l_time
    final_ans['PERCENT'] = l_percent
    return final_ans


