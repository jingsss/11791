from BM25 import BM25

class SentenceRanker2():
    def __init__(self, jsonobj):
        """
        :param sentence_view: json file format of sentence view
        :param token_view: json file format of token view
        """
        self.jsonobj = jsonobj

    def rank_by_jaccard_similarity(self):
        pass

    def rank_by_bm25(self):
        pass

    def jaccard_similartiy(self, str1, str2):
        str1_set, str2_set = set(str1.split()), set(str2.split())
        intersection_set = str1_set.intersection(str2_set)
        return float(len(intersection_set)) / (len(str1_set) + len(str2_set) - len(intersection_set))

def main():
    sentence_ranker = SentenceRanker2('', '')
    print sentence_ranker.jaccard_similartiy('What do you do', 'How are you')

if __name__ == '__main__':
    main()