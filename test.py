#!/usr/bin/python

from sliding_window import *
from annotations.annotator import *
import spacy
from spacy.en import English
from nltk.corpus import wordnet
import phrasemachine

def get_type(word):
	all_type = ["PERSON", "LOCATION", "ORGANIZATION", "DATE","LOCATION", "TIME", "PERCENT"]
	synsets = wordnet.synsets(word)
	if len(synsets) == 0:
		 return None
	else:
		p_tag = str(synsets[0].lexname()).split(".")[1].upper()
		if p_tag in all_type:
			return p_tag
		if p_tag == "QUANTITY":
			return "NUMBER"
			
#q = "Who suggested the hiatus for Beyonce"	
#s = "Beyonce announced a hiatus from her music career in January 2010, heeding her mother's advice, \"to live life, to be inspired by things again\""
#tag = create_annotations(s)
#for i in range(len(tag['tokens'])):
#	if tag['pos'][i] == 'NN':
#		print tag['tokens'][i], get_type(tag['tokens'][i])
##
q = "How many editions of Heat exist?"	
s = "The twenty five editions of Heat are the world's best-selling celebrity fragrance line, with sales of over $400 million."
print best_candidate_token(q, s, "six")

	

