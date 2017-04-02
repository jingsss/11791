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
Sentence2 = "It is a replica of the grotto at Lourdes France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858"
Question = "To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?"
print best_candidate(Sentence2, Question)
