from flask import Flask, jsonify, request
import sys
import json


class SentenceRanker():
    def __init__(self, jsonobj):
        """
        :param sentence_view: json file format of sentence view
        :param token_view: json file format of token view
        """
        # self.jsonobj = jsonobj
        self.top_k = 5  # rank the sentences s.t. we only consider top k candidates
        # with open(self.jsonobj) as data_file:
        #     self.data = json.load(data_file)
        self.data = jsonobj

    def rank_by_jaccard_similarity(self):
        all_views = self.data['payload']['views']
        for each_view in all_views:
            annotations = each_view['annotations']
            question = filter(lambda x: x['id'] == 'Q', annotations)
            ground_truth = filter(lambda x: x['id'] == 'A', annotations)
            candidates = filter(lambda x: x['id'] != 'A' and x['id'] != 'Q', annotations)
            scores = [self.jaccard_similartiy(x['features']['target'], question[0]['features']['target']) for x in
                      candidates]
            ranks = sorted(range(len(scores)), key=lambda x: -scores[x])
            for i in range(len(scores)):
                candidates[ranks[i]]['features']['rank'] = i
            each_view['annotations'] = [x for x in annotations if
                                        x['id'] == 'Q' or x['id'] == 'A' or x['features']['rank'] <= self.top_k - 1]
        pass

    def jaccard_similartiy(self, str1, str2):
        str1_set, str2_set = set(str1.split()), set(str2.split())
        intersection_set = str1_set.intersection(str2_set)
        return float(len(intersection_set)) / (len(str1_set) + len(str2_set) - len(intersection_set))

    def get_data(self):
        return self.data

def main():
    # sentence_ranker = SentenceRanker(sys.argv[1])
    # sentence_ranker.rank_by_jaccard_similarity()
    # mydata = sentence_ranker.get_data()
    # print mydata
    print 'hi'



if __name__ == '__main__':
    main()
