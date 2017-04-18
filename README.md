# 11791

currrent classifier:
11791/question-classification/question-classifier/question_classifier.py

how to run:

python ./question-classification/question-classifier/question_classifier.py ./question-classification/question-classifier/data/train   ./question-classification/question-classifier/data/test/

Question type and testing result:

        +++++++++++++++++++++++++++
                  precision    recall  f1-score   support

        CARDINAL       0.92      0.90      0.91        40
            DATE       1.00      0.98      0.99        47
            DESC       0.82      0.99      0.90       138
          ENTITY       0.82      0.76      0.79        74
           EVENT       1.00      0.67      0.80         3
        LANGUAGE       0.67      1.00      0.80         2
        LOCATION       0.89      0.90      0.90        81
           MONEY       1.00      0.33      0.50         3
    ORGANIZATION       0.67      0.67      0.67         6
         PERCENT       0.67      0.67      0.67         3
          PERSON       0.96      0.93      0.95        59
         PRODUCT       0.80      0.27      0.40        15
        QUANTITY       1.00      0.55      0.71        20

     avg / total       0.88      0.87      0.87       491

Confustion Matrix:



    [[ 36   0   3   0   0   0   0   0   0   1   0   0   0]
     [  0  46   1   0   0   0   0   0   0   0   0   0   0]
     [  0   0 137   0   0   0   0   0   0   0   0   1   0]
     [  0   0  14  56   0   0   2   0   1   0   1   0   0]
     [  0   0   0   1   2   0   0   0   0   0   0   0   0]
     [  0   0   0   0   0   2   0   0   0   0   0   0   0]
     [  0   0   4   3   0   1  73   0   0   0   0   0   0]
     [  0   0   1   0   0   0   1   1   0   0   0   0   0]
     [  0   0   0   1   0   0   1   0   4   0   0   0   0]
     [  0   0   1   0   0   0   0   0   0   2   0   0   0]
     [  0   0   1   2   0   0   0   0   1   0  55   0   0]
     [  0   0   3   4   0   0   3   0   0   0   1   4   0]
     [  3   0   3   1   0   0   2   0   0   0   0   0  11]]


