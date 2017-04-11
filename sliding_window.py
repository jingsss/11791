import nltk
from stat_parser import Parser
import numpy as np
import spacy
import phrasemachine
from annotations.annotator import *
from nltk.corpus import stopwords

def get_over_lap(list1, list2):
	list1 = [i.lower() for i in list1]
	list2 = [i.lower() for i in list2]
	num = len(set(list1).intersection(set(list2)))
	return num
	
def traverseTree(tree,list1,list2, question):
	tmp = tree.leaves()
	num = get_over_lap(tmp, question)
	list1.append(tmp)
	list2.append(num)
	for subtree in tree:
		if type(subtree) == nltk.tree.Tree:
			tmp = subtree.leaves()
			traverseTree(subtree, list1, list2, question)
			
def best_candidate(Sentence, Question):
	parser = Parser()
	tree = parser.parse(Sentence)
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
	parser = Parser()
	tree = parser.parse(Sentence)
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

q = "How many editions of Heat exist?"
s= "The six editions of Heat are the world's best-selling celebrity fragrance line, with sales of over $400 million."
def select_best(Question, Sentence, tagger):	
	c = list(phrasemachine.get_phrases(Question)['counts'])
	Sentence2 = Sentence.lower()
	loc_s = [Sentence2.find(i.lower()) for i in c]
	loc = [Sentence2.find(i.lower()) for i in tagger]
	dist = [sum([abs(i - j) for j in loc_s]) for i in loc]
	return tagger[np.argmin(dist)]

#print best_candidate_token(s, q, '400')
#print create_annotations(q)['pos']



