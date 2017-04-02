from flask import Flask,jsonify,request
import urllib, json
import requests
from collections import OrderedDict
import sys
import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from sliding_window import *
path = sys.path[0]
sys.path.append(path + "/sentence_ranker")
from SentenceRanker import *
sys.path.append(path + "/annotations")
from annotator import *

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
def extract_pair(p):
	idx = [i[1] for i in p]
	group = [i[0] for i in p]
	return [idx,group]

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
		sentences = q_a["passage"][0].strip().split(".")
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
			if a["features"]["type"] != ANS:
				info = create_annotations(a["features"]["target"])
				a["features"]["tokens"] = info["tokens"]
				a["features"]["is_num"] = info["is_num"]
				a["features"]["pos"] = info["pos"]
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
	
@app.route("/answer_extractor",methods=['GET', 'POST'])
def answer_extractor():
	t = request.json
	for view in t["payload"]["views"]:
		view["metadata"]["contains"][URI_SENTENCE]["producer"] = "/answer_extractor"
		view["metadata"]["contains"][URI_SENTENCE]["type"] = "answers annotator component"
		question = ""
		for a in view["annotations"]:
			if a["features"]["type"] == QUES:
				question = a["features"]["target"]
				break
		for a in view["annotations"]:
			if a["features"]["type"] == SENS:
				sentence = a["features"]["target"]
				a["features"]["best_candidate"] = best_candidate(sentence, question)
	return jsonify(t)
if __name__ == "__main__":
	app.run()
