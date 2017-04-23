from flask import Flask,jsonify,request
import urllib, json
import requests
from collections import OrderedDict
import sys
import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from nltk.tokenize import sent_tokenize,word_tokenize
from sliding_window import *
from sentence_ranker.SentenceRanker import *
from annotations.annotator import *

import spacy
import en_core_web_sm

class StanfordNLP:
	def __init__(self):
		self.server = ServerProxy(JsonRpc20(),TransportTcpIp(addr=("127.0.0.1", 9000)))
	def parse(self, text):
		return json.loads(self.server.parse(text))

sys.path.insert(0, './question-classification/question-classifier')
from question_classifier import question_classify

URI_SENTENCE = "http://vocab.lappsgrid.org/Sentence"
SERVER = "http://127.0.0.1:5000/"
ANS = "Answer"
QUES = "Question"
SENS = "Sentence"
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

def this_mean(list1):
	if len(list1) == 0:
		return 0.0
	else:
		return float(sum(list1))/len(list1)

def contain_any_answer(ans, sentence):
	value = sum([int(a in sentence) for a in ans])
	return int(value > 0)
def get_F1(candidate, answer):
	candidate = set(candidate.split(" "))
	answer = set(answer.split(" "))
	a_common = len(candidate.intersection(answer))
	a_precision = float(a_common) / len(candidate)
	a_recall = float(a_common) / len(answer)
	F1_a = 0
	if a_precision + a_recall > 0:
		F1_a = 2 * a_precision * a_recall / (a_precision + a_recall)
	return F1_a
def init_container_as_dict():
	data = {}
	data['discriminator'] = "http://vocab.lappsgrid.org/ns/media/jsonld#lif"
	data['payload'] = {}
	data['payload']['@context'] = "http://vocab.lappsgrid.org/context-1.0.0.jsonld"
	data['payload']['metadata'] = {}
	data['payload']['text'] = {}
	data['payload']['views'] = []
	data['parameters'] = {}
#	json_data = json.dumps(data)
	return data
def new_view():
	view = {}
	view['metadata'] = {}
	view['annotations'] = []
	return view

def new_annotation(aid,uri_type,start = -1 ,end = -1):
	annotation = {}
	annotation["id"] = aid
	annotation["start"] = start
	annotation["end"] = end
	annotation["@type"] = uri_type
	annotation["features"] = {}
	return annotation
def coref(passage):
	nlp = StanfordNLP()
	result = nlp.parse(passage)
#	result = nlp.parse("To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France")
	coref = []
	for i in result['coref']:
		idx = [extract_pair(a)[1] for a in i]
		idx = [item for sublist in idx for item in sublist]
		phrase = [extract_pair(a)[0] for a in i]
		phrase= [item for sublist in phrase for item in sublist]
		coref.append([idx, phrase])
	return coref

def get_coref(coref_list,i):
	c_list = [list(set(c[0])) for c in coref_list if i in c[1]]
	return c_list

def parse_element(jsonobj, component, uri_type = URI_SENTENCE):
	data = init_container_as_dict()
	for q_a in jsonobj["response"]["docs"]:
#	q_a = jsonobj["response"]["docs"][0]
		view = new_view()
		#add metadata
		view["metadata"]["contains"] = {}
		view["metadata"]["contains"][uri_type] = {}
		view["metadata"]["contains"][uri_type]["producer"] = component
		view["metadata"]["contains"][uri_type]["type"] = "input component"
		#annotate question
		ann = new_annotation('Q', uri_type)
		ann['features']['target'] = q_a["question"][0]
		ann['features']['type'] = QUES
		ann['features']['squad_id'] = q_a["id"]
		view["annotations"].append(ann)
		#annotate answer
#		start = int(q_a["true_answers.begin"][0])
#		end = int(q_a["true_answers.end"][0])
		ann = new_annotation('A', uri_type)
		ann['features']['target'] = q_a["true_answers.text"]
		ann['features']['type'] = ANS
		ann['features']['squad_id'] = q_a["id"]
		view["annotations"].append(ann)
#		faster
#		coref_list = coref(q_a["passage"][0])

		sentences = sent_tokenize(q_a["passage"][0])
		sentences = [i for i in sentences if len(i) > 0]
		for i in range(len(sentences)):
			ann = new_annotation('S' + str(i), uri_type)
			ann['features']['target'] = sentences[i].strip()
			ann['features']['type'] = SENS
			ann['features']['squad_id'] = q_a["id"]
#			ann['features']['coref'] = get_coref(coref_list, i)
			view["annotations"].append(ann)
		data['payload']['views'].append(view);
	return data

def tag_question(nlp,sentence):
    doc = nlp(sentence)
    text_list = list()
    label_list = dict()
    for ent in doc.ents:
        if ent.label_ in label_list:
            label_list[ent.label_] = label_list[ent.label_] +  ent.text
        else:
            label_list[ent.label_] = ent.text
        text_list.append(ent.text)
    return label_list





@app.route("/hello", methods=['GET', 'POST'])
def hello():
	return jsonify("hello world")

@app.route("/input_component",methods=['GET', 'POST'])
def input_component():
	t = request.json
	data = parse_element(t,"/input_component",URI_SENTENCE)
	return jsonify(data)

@app.route("/token_annotator",methods=['GET', 'POST'])
def token_annotator():
	t = request.json
	for view in t["payload"]["views"]:
		view["metadata"]["contains"][URI_SENTENCE]["producer"] = "/token_annotator"
		view["metadata"]["contains"][URI_SENTENCE]["type"] = "token annotator component"
		for a in view["annotations"]:
			if a["features"]["type"] == SENS:
				info = create_annotations(a["features"]["target"])
				a["features"]["tokens"] = info["tokens"]
				a["features"]["is_num"] = info["is_num"]
#				a["features"]["pos"] = info["pos"]
				a["features"]["PERCENT"] = info["PERCENT"]
				a["features"]["TIME"] = info["TIME"]
				a["features"]["DATE"] = info["DATE"]
				a["features"]["ORG"] = info["ORG"]
				a["features"]["LOCATION"] = info["LOCATION"]
				a["features"]["PERSON"] = info["PERSON"]
	return jsonify(t)



@app.route("/question_classifier",methods=['GET', 'POST'])
def question_classifier():
	t = request.json
	for view in t["payload"]["views"]:
		view["metadata"]["contains"][URI_SENTENCE]["producer"] = "/question_classifier"
		view["metadata"]["contains"][URI_SENTENCE]["type"] = "question classifier component"
	res = question_classify(t)
		#t = request.json
		#print res
	return jsonify(res)

@app.route("/sentence_ranker",methods=['GET', 'POST'])
def sentence_ranker():
	t = request.json
	sentence_ranker = SentenceRanker(t)
	sentence_ranker.rank_by_jaccard_similarity()
	data = sentence_ranker.get_data()
	return jsonify(data)

def check_valid_candidate(features,question_type):
	ret = []
	if question_type == "ORGANIZATION":
		if len(features["ORG"]) > 0:
			ret = features["ORG"]
	elif question_type == "DATE":
		if len(features["DATE"]) > 0 or len(features["TIME"]) > 0:
			ret = features["DATE"] + features["TIME"]
	elif question_type == "LOCATION":
		if len(features["LOCATION"]) > 0 or len(features["ORG"]) > 0:
			ret = features["LOCATION"] + features["ORG"]
	elif question_type == "PERSON":
		if len(features["PERSON"]) > 0:
			ret = features["PERSON"]
	elif question_type == "PERCENT":
		if len(features["PERCENT"]) > 0:
			ret = features["PERCENT"]
	elif question_type == "NUM":
		ret = [features["toks"][i] for i in len(features["is_num"]) if features["is_num"][i] == True]
	else:
		ret = []
	return ret
@app.route("/answer_extractor",methods=['GET', 'POST'])
def answer_extractor():
	t = request.json
        nlp = en_core_web_sm.load()
        for view in t["payload"]["views"]:
		view["metadata"]["contains"][URI_SENTENCE]["producer"] = "/answer_extractor"
		view["metadata"]["contains"][URI_SENTENCE]["type"] = "answers annotator component"
		question = ""
		for a in view["annotations"]:
			if a["features"]["type"] == QUES:
				question = a["features"]["target"]
				question_type = str(a["features"]["question_type"])
				break
		for a in view["annotations"]:
			if a["features"]["type"] == SENS:
				if a["features"]["rank"] == 0:
					sentence = a["features"]["target"]
					info = create_annotations(sentence)
                                        entity_info = tag_question(nlp,sentence)
					if question_type in info:
						info = info[question_type]
						q = question.lower()
						info = [i for i in info if i.lower() not in q]
                                        elif question_type in entity_info:
						entity_info = entity_info[question_type]
						#info = entity_info.lower()
						q = question.lower()
						info = [i for i in info if i.lower() not in q]
                                        else:
						info = []
					if len(info) > 0:
						candidate = select_best(question, sentence, info)
						a["features"]["select_method"] = "class"
					else:
						candidate = best_candidate(sentence, question)
						a["features"]["select_method"] = "sliding"
					a["features"]["best_candidate"] = candidate
					break
	return jsonify(t)

@app.route("/final_out",methods=['GET', 'POST'])
def final_out():
	t = request.json
	for view in t["payload"]["views"]:
		question = None
		squad_id = None
		candidate = None
#        question_type = ""
		for a in view["annotations"]:
			if a["features"]["type"] == QUES:
				question = a["features"]["target"]
				squad_id = a['features']['squad_id']
				break
		for a in view["annotations"]:
			if a["features"]["type"] == SENS:
				if a["features"]["rank"] == 0:
					sentence = a["features"]["target"]
					candidate = best_candidate(sentence, question)
					break
	return jsonify(squad_id + ":" + candidate)


@app.route("/evaluation",methods=['GET', 'POST'])
def evaluation():
	t = request.json
	for view in t["payload"]["views"]:
		view["metadata"]["contains"][URI_SENTENCE]["producer"] = "/evaluation"
		view["metadata"]["contains"][URI_SENTENCE]["type"] = "evaluation"
		question = None
		answer = None
		candidate = None
		squad_id = None
		sentence = []
		for a in view["annotations"]:
			if a["features"]["type"] == QUES:
				question = a["features"]["target"]
				question = question.lower()
				squad_id = a['features']['squad_id']
			if a["features"]["type"] == ANS:
				answer = a["features"]["target"]
				answer = [a.lower() for a in answer]
		for a in view["annotations"]:
			if a["features"]["type"] == SENS:
				s = a["features"]["target"]
				s = s.lower()
				sentence.append([s, int( a["features"]["rank"])])
				if a["features"]["rank"] == 0:
					candidate = a["features"]["best_candidate"].lower()

		sentence = sorted(sentence,key=lambda x: x[1])
		rel_q = [contain_any_answer(answer, s[0]) for s in sentence]
		p_k = [this_mean(rel_q[0:i+1]) for i in range(len(rel_q))]
		pr = this_mean([p_k[i] for i in range(len(rel_q)) if rel_q[i] > 0])
		first_k = -1
		if pr > 0:
			first_k = rel_q.index(1)
		em = [int(candidate == a) for a in answer]
		F1_a = [get_F1(candidate, a) for a in answer]
#		stats = {}
#		stats["id"] = squad_id
#		stats["precision @ k"] = p_k[0]
#		stats["pr"] = pr
#		stats["em"] = max(em)
#		stats["F1"] = max(F1_a)
		values = [squad_id,p_k[0], first_k, pr, max(em), max(F1_a)]
		values = [str(i) for i in values]
		return jsonify(",".join(values))

if __name__ == "__main__":
	app.run()
