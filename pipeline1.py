#!/usr/bin/python
from flask import Flask,jsonify,request
import urllib, json
import requests
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
def get_from_component(obj, url):
	headers = {'Content-Type' : 'application/json;charset=UTF-8'}
	r = requests.post(url, data=json.dumps(obj), headers=headers)
	obj = r.json()
	return obj

@app.route("/pipeline",methods=['GET', 'POST'])
def pipeline():
	row = int(request.args.get('row'))
	f = "&q=fold:1"
#	f = ""x
	source_url = "http://138.197.73.251:8983/solr/train/select?indent=on&q=*:*&rows=%d&start=%d&wt=json%s"%(1, row,f)
	input_component = "http://127.0.0.1:5000/input_component"
	token_annotator = "http://127.0.0.1:5000/token_annotator"
	question_classifier_url = "http://127.0.0.1:5000/question_classifier"
	sentence_ranker_url = "http://127.0.0.1:5000/sentence_ranker"
	answer_extractor_url = "http://127.0.0.1:5000/answer_extractor"
	final_out_url = "http://127.0.0.1:5000/final_out"
#	print source_url
	r = requests.get(source_url)
	obj = r.json()
	obj = get_from_component(obj, input_component)
#	obj = get_from_component(obj, token_annotator)
#	obj = get_from_component(obj, question_classifier_url)
	obj = get_from_component(obj, sentence_ranker_url)
#	obj = get_from_component(obj, answer_extractor_url)
	obj = get_from_component(obj, final_out_url)
        #print obj
	return jsonify(obj)

@app.route("/pipeline1",methods=['GET', 'POST'])
def pipeline1():
	row = int(request.args.get('row'))
	f = "&q=fold:1"
#	f = ""x
	source_url = "http://138.197.73.251:8983/solr/train/select?indent=on&q=*:*&rows=%d&start=%d&wt=json%s"%(1, row,f)
	input_component = "http://127.0.0.1:5000/input_component"
	token_annotator = "http://127.0.0.1:5000/token_annotator"
	question_classifier_url = "http://127.0.0.1:5000/question_classifier"
	sentence_ranker_url = "http://127.0.0.1:5000/sentence_ranker"
	answer_extractor_url = "http://127.0.0.1:5000/answer_extractor"
	final_out_url = "http://127.0.0.1:5000/final_out"
#	print source_url
	r = requests.get(source_url)
	obj = r.json()
	obj = get_from_component(obj, input_component)
#	obj = get_from_component(obj, token_annotator)
#	obj = get_from_component(obj, question_classifier_url)
	obj = get_from_component(obj, sentence_ranker_url)
	obj = get_from_component(obj, answer_extractor_url)
#	obj = get_from_component(obj, final_out_url)
        #print obj
	return jsonify(obj)
@app.route("/evaluation",methods=['GET', 'POST'])
def evaluation():
	row = int(request.args.get('row'))
	f = "&q=fold:1"
#	f = ""x
	source_url = "http://138.197.73.251:8983/solr/train/select?indent=on&q=*:*&rows=%d&start=%d&wt=json%s"%(1, row,f)
	input_component = "http://127.0.0.1:5000/input_component"
	token_annotator = "http://127.0.0.1:5000/token_annotator"
	question_classifier_url = "http://127.0.0.1:5000/question_classifier"
	sentence_ranker_url = "http://127.0.0.1:5000/sentence_ranker"
	answer_extractor_url = "http://127.0.0.1:5000/answer_extractor"
	evaluation_url = "http://127.0.0.1:5000/evaluation"
#	print source_url
	r = requests.get(source_url)
	obj = r.json()
	obj = get_from_component(obj, input_component)
#	obj = get_from_component(obj, token_annotator)
#	obj = get_from_component(obj, question_classifier_url)
	obj = get_from_component(obj, sentence_ranker_url)
	obj = get_from_component(obj, answer_extractor_url)
	obj = get_from_component(obj, evaluation_url)
	return jsonify(obj)
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8888)