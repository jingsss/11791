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

def question_classify(docs_train, y_train, docs_test1):


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
        #'tfidf__use_idf': (True, False),
        #'tfidf__norm': ('l1', 'l2'),
        'clf__alpha': (0.00001, 0.000001),
        'clf__penalty': ('l2', 'elasticnet'),
        #'clf__n_iter': (10, 50, 80),
    }

    #grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
    #grid_search.fit(docs_train, y_train)
    filename = './classifier.joblib.pkl'
    #_ = joblib.dump(grid_search, filename, compress=9)
    grid_search = joblib.load(filename)

    #print(grid_search.grid_scores_)

    #Predict the outcome on the testing set and store it in a variable
    # named y_predicted
    y_predicted = grid_search.predict(docs_test1)
    return y_predicted

if __name__ == "__main__":
    res = urllib2.urlopen("http://127.0.0.1:8080/pipeline?row=1").read()
    ress =  json.loads(res)
    #for item in ress["payload"]["views"]["annotations"]:
    #    print item
    test_set = list()
    test_set.append(json.dumps(ress['payload']['views'][0]['annotations'][0]['features']['target'], indent=4, sort_keys=True))


    #sys.exit(0)
    # the training data folder must be passed as first argument
    questions_data_folder = sys.argv[1]
    dataset = load_files(questions_data_folder, shuffle=False)
    print("n  training samples: %d" % len(dataset.data))

    # split the dataset in training and test set:
    docs_train, _, y_train, _ = train_test_split(
        dataset.data, dataset.target, test_size=0.0, random_state=None)

    # the testing data folder must be passed as first argument
    questions_data_folder1 = sys.argv[2]
    dataset1 = load_files(questions_data_folder1, shuffle=False)
    print("n testing  samples: %d" % len(dataset1.data))

    # split the dataset in training and test set:
    _, docs_test1, _, y_test = train_test_split(
        dataset1.data, dataset1.target, test_size=499, random_state=None)
    #print y_test
    #print docs_test1
    #print type( docs_test1)

    y_predicted = question_classify(docs_train, y_train, test_set)
    print "+++++++++++++++++++++++++++"
    print y_predicted
    print len(y_predicted)
    print "+++++++++++++++++++++++++++"
    # Print the classification report
    #print(metrics.classification_report(y_test, y_predicted,
    #                                    target_names=dataset.target_names))

    # Print and plot the confusion matrix
    #cm = metrics.confusion_matrix(y_test, y_predicted)
    #print(cm)

    #import matplotlib.pyplot as plt
    #plt.matshow(cm)
    #plt.show()
