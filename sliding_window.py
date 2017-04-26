#-*- coding: utf-8 -*-
import nltk
from stat_parser import Parser
import numpy as np
import spacy
from spacy.en import English
import phrasemachine
from annotations.annotator import *
from nltk.corpus import stopwords
import hashlib
from spacy.symbols import attr,nsubj, NOUN, PROPN


en_nlp = spacy.load('en')
parse_cache = dict()
statt= dict()
def get_md5(Sentence):
    tmp = Sentence.encode("utf-8")
    m = hashlib.md5()
    m.update(tmp)
    return  m.digest()

def get_over_lap(list1, list2):
	list1 = [i.lower() for i in list1]
	list2 = [i.lower() for i in list2]
	num = len(set(list1).intersection(set(list2)))
	return num

def traverseTree(tree,list1,list2, question):
	if any(["NN" in i[1] or "CD" in i[1] for i in tree.pos()]):
			tmp = tree.leaves()
			num = get_over_lap(tmp, question)
			list1.append(tmp)
			list2.append(num)
			for subtree in tree:
				if type(subtree) == nltk.tree.Tree:
					tmp = subtree.leaves()
					traverseTree(subtree, list1, list2, question)
#	tmp = tree.leaves()
#	num = get_over_lap(tmp, question)
#	list1.append(tmp)
#	list2.append(num)
#	for subtree in tree:
#		if type(subtree) == nltk.tree.Tree:
#			tmp = subtree.leaves()
#			traverseTree(subtree, list1, list2, question)

global eval_counter
global eval_f1
global eval_em

statt["eval_counter"] = 0.0
statt["eval_em"] = 0.0
statt["eval_f1"] = 0.0
eval_em = 0
eval_f1 = 0
def calccc(em,F1_a):
    statt["eval_counter"] =  float(statt["eval_counter"]) + 1
    statt["eval_em"] = float(statt["eval_em"]) + float(em)
    statt["eval_f1"] = float(statt["eval_f1"]) + F1_a
    print "current ave em:" + str(statt["eval_em"] / statt["eval_counter"])
    print "current ave f1:" + str(statt["eval_f1"] / statt["eval_counter"])

def best_candidate(Sentence, Question):
        #Sentence = 'Notre Dame\'s most recent when?'

        #Sentence = Sentence.replace('[',' ')
        #Sentence = Sentence.replace(']',' ')
#        print "Sentence: " +  Sentence
        #print Question
        key = get_md5(Sentence)
        if key in parse_cache:
            print "hit"
            tree = parse_cache[key]
        else:
            try:
	        parser = Parser()
                tree = parser.parse(Sentence)
                parse_cache[key] = tree
            except:
                return " "
        list1 = []
	list2 =[]
        traverseTree(tree, list1, list2, Question.split())
	min_overlap = min(list2)
	num = [[i,len(list1[i])] for i in range(len(list1)) if list2[i] == min_overlap]
	s = sorted(num, key = lambda x: -x[1])
	return " ".join(list1[s[0][0]])

def traverseTree_token(tree,list1,list2, question, token):
	tmp = tree.leaves()
	if token in tmp:
		num = get_over_lap(tmp, question)
		list1.append(tmp)
		list2.append(num)
		for subtree in tree:
			if type(subtree) == nltk.tree.Tree:
				tmp = subtree.leaves()
				traverseTree_token(subtree, list1, list2, question, token)
	else:
		return

def best_candidate_token(Sentence, Question, token):
	#parser = Parser()
	#tree = parser.parse(Sentence)

        print "Sentence: " +  Sentence
        key = get_md5(Sentence)
        if key in parse_cache:
            print "hit"
            tree = parse_cache[key]
        else:
            try:
	        parser = Parser()
                tree = parser.parse(Sentence)
                parse_cache[key] = tree
            except:
                return " "
        list1 = []
	list2 =[]
	traverseTree_token(tree, list1, list2, Question.split(),token)
	min_overlap = min(list2)
	num = [[i,len(list1[i])] for i in range(len(list1)) if list2[i] == min_overlap]
	s = sorted(num, key = lambda x: -x[1])
	return " ".join(list1[s[0][0]])

#Sentence2 = unicode("Beyonce has stated that she is personally inspired by US First Lady Michelle Obama, saying \"She proves you can do it all\" and she has described Oprah Winfrey as \"the definition of inspiration and a strong woman\".")
#Question = "Beyonce has said that who embodies the definition of inspiration and a strong woman?"
#s = "Who suggested the hiatus for Beyonce"
#q = "Beyonce announced a hiatus from her music career in January 2010, heeding her mother's advice, \"to live life, to be inspired by things again\""

	
def select_best(Question, Sentence, tagger):
	c = list(phrasemachine.get_phrases(Question)['counts'])
	Sentence2 = Sentence.lower()
	loc_s = [Sentence2.find(i.lower()) for i in c]
	loc_s = [i for i in loc_s if i >= 0]
	if len(loc_s) == 0:
		return tagger[0]
	loc = [Sentence2.find(i.lower()) for i in tagger]
	dist = [sum([abs(i - j) for j in loc_s]) for i in loc]
	return tagger[np.argmin(dist)]

def headword(question):
	head_word = []
	en_doc = en_nlp(u'' + question)
	for sent in en_doc.sents:
		for token in sent:
			if token.dep == nsubj and (token.pos == NOUN or token.pos == PROPN):
				head_word.append(token.text)
			elif token.dep == attr and (token.pos == NOUN or token.pos == PROPN):
				head_word.append(token.text)
	head_word = [i.encode('utf-8') for i in head_word]
	return head_word
	
def distance_between_word(keyword, queryword, sent):
	loc_q = sent.find(queryword)
	loc_k = sent.find(keyword)
	if loc_q > loc_k:
		sub_sent = word_tokenize(sent[loc_k + len(keyword): loc_q])
	else:
		sub_sent = word_tokenize(sent[loc_q + len(queryword) : loc_k])	
	return len(sub_sent)

def select_best_2(Question, Sentence, tagger):
	c = list(phrasemachine.get_phrases(Question)['counts'])
	c = c + headword(Question)
	Sentence2 = Sentence.lower()
	loc_s = [i.lower() for i in c if i.lower() in Sentence]
	if len(loc_s) == 0:
		return tagger[0]
	dist = [sum([distance_between_word(k, q, Sentence) for k in loc_s]) for q in tagger]
	return tagger[np.argmin(dist)]
	
#print create_annotations(q)['pos']



