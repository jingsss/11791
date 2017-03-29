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
	source_url = "http://138.197.73.251:8983/solr/train/select?indent=on&q=*:*&rows=%d&start=%d&wt=json"%(row, row - 1)
	input_component = "http://127.0.0.1:5000/input_component"
	annotator = "http://127.0.0.1:5000/annotator"
	r = requests.get(source_url)
	obj = r.json()
	obj = get_from_component(obj, input_component)
	obj = get_from_component(obj, input_component)
	return jsonify(obj)

if __name__ == "__main__":
	app.run(port=8080)