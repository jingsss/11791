from flask import Flask,jsonify,request
import urllib, json
import requests
from collections import OrderedDict
URI_SENTENCE = "http://vocab.lappsgrid.org/Sentence"
SERVER = "http://127.0.0.1:5000/"
ANS = "Answer"
QUES = "Question"
SENS = "Sentence"
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
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
		#annotate passage
		
		sentences = q_a["passage"][0].strip().split(".")
		sentences = [i for i in sentences if len(i) > 0]
		for i in range(len(sentences)):
			ann = new_annotation('S' + str(i), uri_type)
			ann['features']['target'] = sentences[i].strip()
			ann['features']['type'] = SENS
			ann['features']['squad_id'] = q_a["id"]
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
	
@app.route("/annotator",methods=['GET', 'POST'])
def annotator():
	t = request.json
	for view in t["payload"]["views"]:
		view["metadata"]["contains"][URI_SENTENCE]["producer"] = "/annotator"
		view["metadata"]["contains"][URI_SENTENCE]["type"] = "annotator component"
		for a in view["annotations"]:
			if a["features"]["type"] != ANS:
				a["features"]["tokens"] = a["features"]["target"].split()
	return jsonify(t)
	


if __name__ == "__main__":
	app.run()