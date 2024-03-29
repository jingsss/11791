# 11-791 Annotations using the  NLTK Library
import nltk
from nltk import word_tokenize
from nltk.tag.stanford import StanfordNERTagger
import re 
from nltk.corpus import wordnet

import unicodedata
import spacy
nlp = spacy.load('en')

#nltk.download("words")
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
classifier = './stanford/classifiers/english.muc.7class.distsim.crf.ser.gz'
jar = './stanford/stanford-ner.jar'
st = StanfordNERTagger(classifier,jar)
#

# Tokenizes and returns pos tags for each token
# function call
# pos_tags("The house is painted blue")

# output
# List if tuples
# [('The', 'DT'), ('house', 'NN'), ('is', 'VBZ'), ('painted', 'VBN'), ('blue', 'JJ')]
def get_type(word):
    all_type = ["PERSON", "LOCATION", "ORGANIZATION", "DATE", "TIME", "PERCENT"]
    synsets = wordnet.synsets(word)
    if len(synsets) == 0:
         return None
    else:
        p_tag = str(synsets[0].lexname()).split(".")[1].upper()
        if p_tag in all_type:
            return p_tag

def tokenize(sent):
    text = nltk.word_tokenize(sent)
    return text

def pos_tags(text):
    #text =  tokenize(sent)
    text2 = nltk.pos_tag(text)
    poss= []
    for a in text2:
        poss.append(a[1])
    # print poss
    return poss


def named_ent2(tagged):
    # tagged = tokenize(sent)
    namedEnt = st.tag(tagged)
    #print namedEnt
    #namedEnt.draw()
    print "NER"
    print namedEnt

    return namedEnt


def calc_tags(s):
    doc = nlp(unicode(s))
    # print "SPACY"
    loc = [] # facility, gpe,loc
    person = [] # person,
    org = [] # norp, org
    product = [] # prod , work of art , language
    event = [] # event 
    date = [] #date 
    time = [] # time 
    num = [] # ppercent, money, quantity, ordinal , cardinal
    f_tok = []  
    # print doc
    doc2 = nlp.tokenizer(unicode(s))
    # for word in doc:
    #     print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)
    # #print type(doc2)


    allent = []
    for ent in doc.ents:
        # print ent.label_, ent.text
        if ent.label_ == "GPE"  or \
            ent.label_ == "LOC" or \
            ent.label_ == "FACILITY" :
            loc.append(ent.text)

        elif ent.label_ == "PERSON":
            person.append(ent.text)

        elif ent.label_ == "NORP"  or \
            ent.label_ == "ORG":
            org.append(ent.text)

        elif ent.label_ == "PRODUCT"  or \
            ent.label_ == "WORK_OF_ART" or \
            ent.label_ == "LANGUAGE" :
            product.append(ent.text)

        elif ent.label_ == "EVENT" :
            event.append(ent.text)
        elif ent.label_ == "DATE":
            date.append(ent.text)

        elif ent.label_ == "TIME":
            time.append(ent.text)
        elif ent.label_ == "PERCENT" or \
            ent.label_ == "MONEY" or \
            ent.label_ == "QUANTITY" or \
            ent.label_ == "ORDINAL" or \
            ent.label_ == "CARDINAL":
            num.append(ent.text)
    # allent = loc+person+org+ product + event+ date+ time+ num 

    # alls = [] 

    # for x in doc2:
    #     print x 
    #     if x not in allent:
    #         sub = ""
    #         alls.append(x)
    #     else:
    #         sub =+ x

    # print alls





        # if x not in list(doc.ents):
        #     print x
        #     f_tok.append(x)

    # print f_tok
    
    return loc, person,org, product, event,date, time, num

def norms(k):
    for x in k:
        x[1].encode('ascii','ignore')
    return k

def get_entity_mod(k2, ent):
    l = []
    tok_mod = []
    s = ""
    for x in k2:
        # print x
        if x[1] == ent:
            # print "isent"
            s += x[0].encode('ascii','ignore') +" "
        else:
            if s == "":
                tok_mod.append(x)
                # print x

                continue
            else:
                #print s
                if s[-1] == " ":
                    s2 = s[:-1]
                else:
                    s2 = s

                l.append(s2)

                tok_mod.append((s,ent))
                tok_mod.append(x)
                # print "elsE",s2
                s = ""
            #l.append(x[0].encode('ascii','ignore'))

    if s != "":
        if s[-1] == " ":
            s2 = s[:-1]
        else:
            s2 = s
        l.append(s2)
        tok_mod.append((s,ent))
    # print tok_mod
    #print l
    return l,tok_mod

def all_entity(k2):
    # print k2
    # print "###############################################"
    l_org,k2 = get_entity_mod(k2,"ORGANIZATION")
    # print k2
    # print "###############################################"
    l_date,k2 = get_entity_mod(k2,"DATE")
    # print k2
    # print "###############################################"
    l_person,k2= get_entity_mod(k2,"PERSON")
    # print k2
    # print "###############################################"
    l_loc,k2 = get_entity_mod(k2,"LOCATION")
    # print k2
    # print "###############################################"
    l_percent,k2 = get_entity_mod(k2,"PERCENT")
    # print k2
    # print "###############################################"
    l_time, k2 = get_entity_mod(k2,"TIME")
    # print "###############################################"
    return l_org, l_date, l_person, l_loc, l_percent, l_time,k2


def hasNumbers(k):
    l = []
    for inputString in k:
        t = any(char.isdigit() for char in inputString)
        #print
        l.append(t)

    return l

# main function
#tokenize, POS tags, is num , NER Tags
def create_annotations(sentence):

    final_ans = {}

    # print tokens
    # tokens = [w.replace('pm', 'p.m.') for w in tokens]
    # tokens = [w.replace('am', 'a.m.') for w in tokens]
    replacements = {'am':'a.m.', 
                'pm':'p.m.'}
    s2 = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements), replace, sentence) 
    # print s2 
    loc, person,org, product, event,date, time, num = calc_tags(s2)
    # print "org",org
    # print "date",date
    # print "person",person
    # print "loc", loc
    # print "time",time
    # print "prod", product
    # print "event", event
    # print "num", num

    new_tok = tokenize(s2)
    # k2 = named_ent2(tokens)


    # # print pos_tags(tokens)
    # # final_ans['tokens'] = tokens
    # # final_ans['pos'] = pos_tags(tokens)
    # l_org, l_date, l_person, l_loc, l_percent, l_time,mod_tok  = all_entity(k2)
    # print "org",l_org
    # print "date",l_date
    # print "person",l_person
    # print "loc", l_loc
    # print "%",l_percent
    # print "time",l_time
    # print mod_tok
#    Code for including synset informaton from word net into the ans extractor #
#
#
#    all_entity_tokens = l_org + l_date +l_person +l_loc + l_percent +l_time
#    k = []
#    # for w in mod_tok:
#    #     print "klist"
#    #     print w
#    #     print type(w)
#    #     print w[0]
#
#    #     exit() 
#    mod_tok_mod = [w[0] for w in mod_tok]
#    # print "all_entity_tokens",all_entity_tokens
#    ftok = list(set(mod_tok_mod) - set(all_entity_tokens))
#    # print "all_entity_tokens",all_entity_tokens
#    # print "mod tok",mod_tok_mod
#
#    # print "ftok", ftok
#    # print "ftok0", ftok[0]
#    # print get_type(ftok[0])
#    for w in ftok:
#        new_ent = get_type(w)
#        if new_ent == "PERSON":
#            # print w
#            l_person.append(w)
#        elif new_ent == "LOCATION":
#            l_loc.append(w)
#            # print w
#        elif new_ent == "ORGANIZATION":
#            l_org.append(w)
#            # print w
#        elif new_ent == "DATE":
#            l_date.append(w)
#            # print w
#        elif new_ent == "TIME":
#            l_time.append(w)
#            # print w
#        elif new_ent == "PERCENT":
#            l_percent.append(w)
#            # print w

    # final_ans['is_num'] = hasNumbers(k2)
    final_ans['ORGANIZATION'] = org
    final_ans['PERSON'] = person
    final_ans['DATE'] = date
    final_ans['LOCATION'] = loc
    final_ans['TIME'] = time
    final_ans['PRODUCT'] = product
    final_ans['EVENT'] = event
    #final_ans[''] = l_percent
    # new_tok = []
    # for x in mod_tok:
    #     if x[0][-1] == " "  :
    #         s2 = x[0][:-1]
            
    #     else:
    #         s2 = x[0]
    #         # print s2



    #     new_tok.append(s2)

    final_ans['tokens'] = new_tok

    # print final_ans['tokens']
    final_ans['pos'] = pos_tags(new_tok)
    # nos = hasNumbers(new_tok)
    # final_ans['NUM'] = nos
    # ctr = 0
    # # gets all the numbers in the sentence
    # all_num = []
    # for x in nos:
    #     if x:
    #         all_num.append(new_tok[ctr])
    #         # print 'yay', ctr
    #         # print  new_tok[ctr]
    #         # print l
    #     ctr += 1
    # print all_num
    # gets all entities from percent, time, date
    # all_num_sub = l_date+ l_time + l_percent
    # # print all_num_sub

    # l_number= list(set(all_num) - set(all_num_sub))
    # print l_number
    final_ans['NUMBER'] = num






    return final_ans
def replace(match):
    replacements = {'am':'a.m.', 
                'pm':'p.m.'}
    return replacements[match.group(0)]



#S ="Jack Brown studies at 4 Stony Brook University in New York since 1999 with 90% percentile at 5:00 pm in the evening in Oxford University. He is a student"
#print create_annotations(S)

# This sentence has a grammatical error in the data 
# S ="The Mitsubishi Electric Company Managing Director eat ramen"
#S= "It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858."
#print create_annotations(S)


