from flask import Flask,jsonify,request
import urllib, json
import requests
from collections import OrderedDict
URI_SENTENCE = "http://vocab.lappsgrid.org/Sentence"
SERVER = "http://127.0.0.1:5000/"
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

def parse_element(jsonobj, uri_type = URI_SENTENCE):
	q_a = jsonobj["response"]["docs"][0]
	data = init_container_as_dict()
	view = new_view()
	#add metadata
	view["metadata"]["contains"] = {}
	view["metadata"]["contains"][uri_type] = {}
	view["metadata"]["contains"][uri_type]["producer"] = "/getdata"
	view["metadata"]["contains"][uri_type]["type"] = "input component"
	#annotate question
	ann = new_annotation('Q', uri_type)
	ann['features']['target'] = q_a["question"][0]
	ann['features']['type'] = "Question"
	ann['features']['squad_id'] = q_a["id"]
	view["annotations"].append(ann)
	#annotate answer
	start = int(q_a["true_answers.begin"][0])
	end = int(q_a["true_answers.end"][0])
	ann = new_annotation('A', uri_type, start,end)
	ann['features']['target'] = q_a["true_answers.text"][0]
	ann['features']['type'] = "Answer"
	ann['features']['squad_id'] = q_a["id"]
	view["annotations"].append(ann)
	#annotate passage
	ann = new_annotation('P', uri_type)
	ann['features']['target'] = q_a["passage"][0]
	ann['features']['type'] = "Passage"
	ann['features']['squad_id'] = q_a["id"]
	view["annotations"].append(ann)
	data['payload']['views'].append(view);
	return data
@app.route("/hello", methods=['GET', 'POST'])
def hello():
	return "hello world"

@app.route("/input_component",methods=['GET', 'POST'])
def input_component():
	row = int(request.args.get('row'))
	url = "http://138.197.73.251:8983/solr/train/select?indent=on&q=*:*&rows=%d&start=%d&wt=json"%(row, row - 1)
	r = requests.get(url)
	t = r.json()
	data = parse_element(t, URI_SENTENCE)
	return jsonify(data)
	
@app.route("/annotator",methods=['GET', 'POST'])
def annotator():
	
	return "annotator"
	
if __name__ == "__main__":
	app.run()