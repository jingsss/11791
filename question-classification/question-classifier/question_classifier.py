"""Build a simple Question Classifier using TF-IDF or Bag of Words Model"

"""
import json
import sys
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.externals import joblib
import urllib2

import codecs
def question_classifier_train(docs_train, y_train, docs_test):


    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier()),
    ])

    # uncommenting more parameters will give better exploring power but will
    # increase processing time in a combinatorial way
    parameters = {
        'vect__max_df': (0.5, 0.75, 1.0),
        #'vect__max_features': (None, 5000, 10000, 50000),
        'vect__ngram_range': ((1, 1), (1, 2), (1, 3)),  # unigrams or bigrams
        'tfidf__use_idf': (True, False),
        'tfidf__norm': ('l1', 'l2'),
        'clf__alpha': (0.00001, 0.000001),
        'clf__penalty': ('l2', 'elasticnet'),
        #'clf__n_iter': (10, 50, 80),
    }

    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
    grid_search.fit(docs_train, y_train)
    filename = './classifier_new_try_it_if_you_got_free_time.joblib.pkl'
    _ = joblib.dump(grid_search, filename, compress=9)
    #grid_search = joblib.load(filename)

    print(grid_search.grid_scores_)

    #Predict the outcome on the testing set and store it in a variable
    # named y_predicted
    y_predicted = grid_search.predict(docs_test)
    return y_predicted

def tag_pre_process(PrimaryTag,SubTag):
    res = ""
    if PrimaryTag == "NUM":
        if SubTag == "date":
            res = "DATE"
        elif SubTag == "perc":
            res = "PERCENT"
        else:
            res = "NUMBER"
    elif PrimaryTag == "HUM":
        if SubTag == "gr":
            res = "ORGANIZATION"
        else:
            res = "PERSON"
    elif PrimaryTag == "ENTY":
        res = "ENTITY"
    elif PrimaryTag == "LOC":
        res = "LOCATION"
    elif PrimaryTag == "ABBR":
        res = "OTHER"
    #    if SubTag == "abb":
    #        res = "ABBREVIATION"
    #    elif SubTag == "exp":
    #        res = "EXPLAINATION"
    else:
        res = PrimaryTag
    return res
def question_classifier_predict(docs_test1):


    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier()),
    ])

    # uncommenting more parameters will give better exploring power but will
    # increase processing time in a combinatorial way
    parameters = {
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__max_features': (None, 5000, 10000, 50000),
        'vect__ngram_range': ((1, 1), (1, 2), (1, 3)),  # unigrams or bigrams
        'tfidf__use_idf': (True, False),
        'tfidf__norm': ('l1', 'l2'),
        'clf__alpha': (0.00001, 0.000001),
        'clf__penalty': ('l2', 'elasticnet'),
        'clf__n_iter': (10, 50, 80),
    }

    filename = './classifier.joblib.pkl'
    grid_search = joblib.load(filename)
    y_predicted = grid_search.predict(docs_test1)
    return y_predicted[0]


def question_classify(inputs):
    test_set = list()
    for view in  inputs['payload']['views']:
        for anno in  view['annotations']:
            if anno['id'] == "Q":
                test_set.append(anno['features']['target'])
                y_predicted = question_classifier_predict(test_set)
                anno['features']['question_type'] = str(y_predicted)
                del test_set[:]
    return inputs

if __name__ == "__main__":
    print "question classifier input :  \n"

    docs_train = list()
    y_train = list()
    y_test = list()
    docs_test = list()

    fname = "./question-classification/question-classifier/data/train_5500.label.txt"
    with codecs.open(fname, encoding='utf-8', errors='ignore') as f:
        content = f.readlines()
    for line in content:
        splited = line.split(' ', 1 )
        PrimaryTag = splited[0].split(':',1)[0]
        SubTag = splited[0].split(':',1)[1]
        Tag = splited[0]
        Text = splited[1]
        if tag_pre_process(PrimaryTag,SubTag) == "OTHER":
            continue
        docs_train.append(Text)
        y_train.append(tag_pre_process(PrimaryTag,SubTag))
        #print PrimaryTag
        #print SubTag

    fname = "./question-classification/question-classifier/data/TREC_10.label.txt"
    with codecs.open(fname, encoding='utf-8', errors='ignore') as f:
        content = f.readlines()
    #content = [x.strip() for x in content]
    for line in content:
        splited = line.split(' ', 1 )
        PrimaryTag = splited[0].split(':',1)[0]
        SubTag = splited[0].split(':',1)[1]
        Tag = splited[0]
        Text = splited[1]

        if tag_pre_process(PrimaryTag,SubTag) == "OTHER":
            continue
        docs_test.append(Text)
        y_test.append(tag_pre_process(PrimaryTag,SubTag))
        #print PrimaryTag
        #print SubTag

    print docs_test
    print docs_train
    print y_test
    print y_train

    y_predicted = question_classifier_train(docs_train, y_train, docs_test)
    print "+++++++++++++++++++++++++++"
    print y_predicted
    print len(y_predicted)
    print "+++++++++++++++++++++++++++"
    # Print the classification report
    print(metrics.classification_report(y_test, y_predicted))

    # Print and plot the confusion matrix
    cm = metrics.confusion_matrix(y_test, y_predicted)
    print(cm)

