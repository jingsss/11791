# 11791

currrent classifier:
11791/question-classification/question-classifier/question_classifier.py

how to run:

python ./question-classification/question-classifier/question_classifier.py ./question-classification/question-classifier/data/train   ./question-classification/question-classifier/data/test/


Question type and testing result:

    +++++++++++++++++++++++++++
                  precision    recall  f1-score   support

    ABBREVIATION       1.00      1.00      1.00         1
            DATE       1.00      0.98      0.99        47
            DESC       0.79      0.99      0.88       138
          ENTITY       0.89      0.71      0.79        94
    EXPLAINATION       1.00      0.62      0.77         8
        LOCATION       0.88      0.91      0.90        81
          NUMBER       1.00      0.81      0.89        63
    ORGANIZATION       0.67      0.67      0.67         6
         PERCENT       0.67      0.67      0.67         3
          PERSON       0.98      0.93      0.96        59

     avg / total       0.90      0.88      0.88       500

Confustion Matrix:


    [[  1   0   0   0   0   0   0   0   0   0]
     [  0  46   1   0   0   0   0   0   0   0]
     [  0   0 137   1   0   0   0   0   0   0]
     [  0   0  20  67   0   5   0   1   0   1]
     [  0   0   3   0   5   0   0   0   0   0]
     [  0   0   4   3   0  74   0   0   0   0]
     [  0   0   6   1   0   4  51   0   1   0]
     [  0   0   0   1   0   1   0   4   0   0]
     [  0   0   1   0   0   0   0   0   2   0]
     [  0   0   1   2   0   0   0   1   0  55]]
