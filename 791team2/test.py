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

from __future__ import print_function

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
