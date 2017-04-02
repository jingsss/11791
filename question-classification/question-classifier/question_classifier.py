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
    filename = './classifier.joblib.pkl'
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
        if SubTag == "abb":
            res = "ABBREVIATION"
        elif SubTag == "exp":
            res = "EXPLAINATION"
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
        #'vect__max_features': (None, 5000, 10000, 50000),
        'vect__ngram_range': ((1, 1), (1, 2), (1, 3)),  # unigrams or bigrams
        'tfidf__use_idf': (True, False),
        'tfidf__norm': ('l1', 'l2'),
        'clf__alpha': (0.00001, 0.000001),
        'clf__penalty': ('l2', 'elasticnet'),
        #'clf__n_iter': (10, 50, 80),
    }

    filename = './classifier.joblib.pkl'
    grid_search = joblib.load(filename)
    y_predicted = grid_search.predict(docs_test1)
    return y_predicted


def question_classify(inputs):
    res_cat = ['ABBR','DESC','ENTY','HUM','LOC','NUM']
    #res = urllib2.urlopen("http://127.0.0.1:8888/pipeline?row=" + row_num).read()
#    print "question classifier input :  \n"
    #print inputs
    #print json.dumps(inputs, indent=4, sort_keys=True)
    #ress =  json.loads(str(inputs))
    #for item in ress["payload"]["views"]["annotations"]:
    #    print item


    test_set = list()
    for view in  inputs['payload']['views']:
        for anno in  view['annotations']:
            if anno['id'] == "Q":
#                print anno['features']['target']

                test_set.append(anno['features']['target'])
#                print test_set


                y_predicted = question_classifier_predict(test_set)
#                print y_predicted
                anno['features']['question_type'] = str(y_predicted)
                del test_set[:]
    #print json.dumps(inputs, indent=4, sort_keys=True)
    #print y_predicted
    return inputs

#def question_classify_main(inputs):

if __name__ == "__main__":
    print "question classifier input :  \n"

    docs_train = list()
    y_train = list()
    y_test = list()
    docs_test = list()

    #questions_data_folder = sys.argv[1]
    #dataset = load_files(questions_data_folder, shuffle=False)
    #print("n  training samples: %d" % len(dataset.data))
    fname = "./question-classification/question-classifier/data/train_5500.label.txt"
    with codecs.open(fname, encoding='utf-8', errors='ignore') as f:
        content = f.readlines()
    #content = [x.strip() for x in content]
    for line in content:
        splited = line.split(' ', 1 )
        PrimaryTag = splited[0].split(':',1)[0]
        SubTag = splited[0].split(':',1)[1]
        Tag = splited[0]
        Text = splited[1]
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

        docs_test.append(Text)
        y_test.append(tag_pre_process(PrimaryTag,SubTag))
        #print PrimaryTag
        #print SubTag

    print docs_test
    print docs_train
    print y_test
    print y_train
    # you may also want to remove whitespace characters like `\n` at the end of each line
    #content = [x.strip() for x in content]

    # split the dataset in training and test set:
    #docs_train, _, y_train, _ = train_test_split(
    #    dataset.data, dataset.target, test_size=0.0, random_state=None)

    # the testing data folder must be passed as first argument
    #questions_data_folder1 = sys.argv[2]
    #dataset1 = load_files(questions_data_folder1, shuffle=False)
    #print("n testing  samples: %d" % len(dataset1.data))

    # split the dataset in training and test set:
    #_, docs_test1, _, y_test = train_test_split(
    #    dataset1.data, dataset1.target, test_size=499, random_state=None)

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

