from __future__ import print_function
import json
import numpy as np
from fbpathtrain import VectorizedData
import random
import re
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
import sys
import time
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
import sys
from sklearn import cross_validation

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
def q_to_fdict(q):
    fdict = {}
    for lat in q['LAT']:
        if (lat['type'] != "WordnetLAT"):
            fdict['lat/' + lat['text'] + '/' + lat['type']] = 1
    for sv in q['SV']:
        fdict['sv'] = sv
    if (len(q['SV']) == 0):
        fdict['sv_not_present'] = 1
#     print (fdict)
    return fdict
with open('data/train-data.json', 'r') as f:
    fdict = [q_to_fdict(q) for q in json.load(f)]
    Xdict = DictVectorizer()
    trainX = Xdict.fit_transform(fdict)

with open('data/test-data.json', 'r') as f:
    fdict = [q_to_fdict(q) for q in json.load(f)]
    testX = Xdict.transform(fdict)
with open('data/train-data.tsv', 'r') as f:
    trainY = [line.split("\t")[3].replace("\n","") for line in f]

with open('data/test-data.tsv', 'r') as f:
    testY = [line.split("\t")[3].replace("\n","") for line in f]


cfier = LogisticRegression(solver='lbfgs', multi_class='multinomial')
cfier.fit(trainX, trainY)
print (cfier.score(trainX, trainY))

#Temporary solution: cross validation
res = cross_validation.cross_val_score(cfier, trainX, trainY, cv=10)
print ("10 fold cross-validation accuracy:")
print (res)
print ("Average over folds")
print (sum(res) / float(len(res)))
print ("Accuracy on test data set")
print (cfier.score(testX, testY))
cfier.coef_.tolist

#Error analysis
testX[0]
s = set()
[s.add(e) for e in trainY]
print (sorted(s))
with open('data/test-data.tsv', 'r') as f:
    for i, line in enumerate(f):
        if (cfier.predict(testX[i]) != testY[i]):
            splitted = line.replace("\n", "").split("\t")
            idxs = []
            for key in fdict[i]:
                if (key == 'sv'):
                    key = key + "=" + fdict[i][key]
                idxs.append(Xdict.feature_names_.index(key) if key in Xdict.feature_names_ else 'Not present')
            coefs = [[c[idx] for c in cfier.coef_] if idx != 'Not present' else 'Not present' for idx in idxs]
            print (splitted[0], splitted[2], splitted[3], cfier.predict(testX[i]), fdict[i])
            print ("Class coeficients for LATs and SV:" + str(coefs))
            print ()
with open('data/yoda-questions.json', 'r') as f:
    fdict = [q_to_fdict(q) for q in json.load(f)]
    testX = Xdict.transform(fdict)

with open('data/yoda-questions.tsv', 'r') as f:
    for i, line in enumerate(f):
        print (i, line.replace("\n", ""), cfier.predict(testX[i]), fdict[i])


import math
idx = 27
cls = 4
print (cfier.predict(testX[idx]))
pred = cfier.predict_proba(testX[idx])[0]
print (sum(pred))
print (pred)
res = [1.0 / (1.0 + math.exp(-cfier.intercept_[cls] - testX.getrow(idx).dot(cfier.coef_[cls]))) for cls in range(6)]
print (res)
print ([r/sum(res) for r in res])

import gensim

word_vector_path = "data/glove.6B.50d.txt"
word_vector = gensim.models.KeyedVectors.load_word2vec_format(word_vector_path, binary=False)

def create201dim_vectors(json_filename, tsv_filename):
    with open(json_filename, 'r') as f:
        json_dict = json.load(f)

    res = []
    with open(tsv_filename, 'r') as f:
        for i, line in enumerate(f):
            question = line.split("\t")[2].lower()
            try:
                first_word_vec = word_vector[question.split(" ")[0]]
            except KeyError:
                first_word_vec = np.zeros(50)
            try:
                second_word_vec = word_vector[question.split(" ")[1]]
            except KeyError:
                second_word_vec = np.zeros(50)
            lat_array = [lat['text'] for lat in json_dict[i]['LAT'] if lat['type'] != "WordnetLAT"]
            sv_array = json_dict[i]['SV']
            lat_vec = np.zeros(50)
            for w in lat_array:
                try:
                    tmp = word_vector[w.lower()]
                except:
                    tmp = np.zeros(50)
                lat_vec = lat_vec + tmp
            if (len(lat_array) != 0):
                lat_vec = lat_vec / float(len(lat_array))
            else:
                lat_vec = np.zeros(50)
#             lat_vec = np.mean([word_vector[w.lower()] if w.lower() in word_vector else np.zeros(50) for w in lat_array], axis=0)
#             print lat_vec
#             if (len(lat_array) == 1 and lat_array[0].lower() in word_vector):
#                 lat_vec = word_vector[lat_array[0].lower()]
#             else:
#                 lat_vec = np.zeros(50)
            if (len(sv_array) == 1 and sv_array[0].lower() in word_vector):
                sv_vec = word_vector[sv_array[0].lower()]
                flag = 0
            else:
                sv_vec = np.zeros(50)
                flag = 1
            vec = np.concatenate((first_word_vec, second_word_vec, lat_vec, sv_vec, np.zeros(1) + flag))
            res.append(vec)
    return res

#201 dimensional vectors; vectors of first two words from question plus LAT and SV



train200vectors = create201dim_vectors('data/train-data.json', 'data/train-data.tsv')

cfier = LogisticRegression(solver='lbfgs', multi_class='multinomial')
cfier.fit(train200vectors, trainY)

test200vectors = create201dim_vectors('data/test-data.json', 'data/test-data.tsv')

cfier.score(test200vectors, testY)

print (len(train200vectors))
print (len(test200vectors))
# print (testX)
from scipy.sparse import hstack
mergedTrain = hstack((train200vectors, trainX))
mergedTest = hstack((test200vectors, testX))


cfier = LogisticRegression(solver='lbfgs', multi_class='multinomial')
cfier.fit(mergedTrain, trainY)

print (cross_validation.cross_val_score(cfier, mergedTrain, trainY, cv=10))
print (cfier.score(mergedTest, testY))
testX

#Error analysis

#TODO: Table of weights of features, most similar words to segments of weight vector
with open('data/test-data.json', 'r') as f:
    json_dict = json.load(f)

with open('data/test-data.tsv', 'r') as f:
    for i, line in enumerate(f):
        if (cfier.predict(mergedTest.getrow(i)) != testY[i]):
            print (line.replace("\n", ""), cfier.predict(mergedTest.getrow(i)), json_dict[i]['SV'], [lat['text'] for lat in json_dict[i]['LAT'] if lat['type'] != "WordnetLAT"])


idx = 0
s = set()
[s.add(e) for e in trainY]
s = sorted(s)
# print (cfier.predict(test200vectors[idx]))
# print (cfier.predict_proba(test200vectors[idx]))

for i, weight_vector in enumerate(cfier.coef_):
    print ("Class name: " + s[i])
    print ("First word:")
    print (word_vector.most_similar(positive=[weight_vector[:50]]))
    print ("Second word:")
    print (word_vector.most_similar(positive=[weight_vector[50:100]]))
    print ("Support verb:")
    print (word_vector.most_similar(positive=[weight_vector[100:150]]))
    print ("LAT:")
    print (word_vector.most_similar(positive=[weight_vector[150:200]]))
    print ("SV not present flag:")
    print (weight_vector[200:201])
