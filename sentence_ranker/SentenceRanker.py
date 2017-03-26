class SentenceRanker():
    def __init__(self, sentence_view, token_view):
        """
        :param sentence_view: json file format of sentence view
        :param token_view: json file format of token view
        """
        self.sentence_view, self.token_view = sentence_view, token_view

    def rank_by_Jaccard(self):
        pass

    def rank_by_BM25(self):
        pass
