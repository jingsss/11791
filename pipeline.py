#!/usr/bin/python
from flask import Flask,jsonify,request
import urllib, json
import requests
from collections import OrderedDict
URI_SENTENCE = "http://vocab.lappsgrid.org/Sentence"
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
@app.route("/pipeline",methods=['GET', 'POST'])
def pipeline():
	row = int(request.args.get('row'))
	url = "http://138.197.73.251:8983/solr/train/select?indent=on&q=*:*&rows=%d&start=%d&wt=json"%(row, row - 1)
	r = requests.get(url)
	obj = r.json()
	url = "http://127.0.0.1:5000/input_component"
	headers = {'Content-Type' : 'application/json;charset=UTF-8'}
	r = requests.post(url, data=json.dumps(obj), headers=headers)
	obj = r.json()
	return jsonify(obj)

if __name__ == "__main__":
	app.run(port=8080)