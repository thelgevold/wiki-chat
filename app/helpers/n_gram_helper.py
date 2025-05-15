from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict

class NGramHelper:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NGramHelper, cls).__new__(cls)
        return cls.instance

    def initialize_vectorizer(self, text_chunks: list[str]):
        self.vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words="english")
        X = self.vectorizer.fit_transform(text_chunks)
        ngrams = self.vectorizer.get_feature_names_out()

        self.inverted_index = defaultdict(set)

    def add_to_inverted_index(self, chunk: str, idx: int):
        tokens = self.vectorizer.build_analyzer()(chunk)
        for n in range(1, 4):
            for i in range(len(tokens) - n + 1):
                ngram = ' '.join(tokens[i:i+n])
                self.inverted_index[ngram].add(idx)
            
    def match_query_ngrams(self, query: str):    
        query_tokens = self.vectorizer.build_analyzer()(query)

        matched_chunks = defaultdict(int)

        for n in range(1, 4):
            for i in range(len(query_tokens) - n + 1):
                ngram = ' '.join(query_tokens[i:i+n])
                for idx in self.inverted_index.get(ngram, []):
                    matched_chunks[idx] += 1

        # Rank by frequency of matched n-grams
        return sorted(matched_chunks.items(), key=lambda x: -x[1])