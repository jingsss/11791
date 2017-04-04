import nltk
from stat_parser import Parser
import numpy as np

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
#	print tmp
#	print num
	for subtree in tree:
		if type(subtree) == nltk.tree.Tree:
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
#Sentence2 = unicode("In ice hockey, the Irish were forced to find a new conference home after the Big Ten Conference's decision to add the sport in 2013-14 led to a cascade of conference moves that culminated in the dissolution of the school's former hockey home, the Central Collegiate Hockey Association, after the 2012-13 season.")
#Question = "Where did the Fighting Irish hockey team compete prior to a move to Hockey East, in terms of conference?"
#print best_candidate(Sentence2, Question)
