from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
import json

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
       
        for token in tokens:
            self.inverted_index[token].add(idx)
            
    def match_query_ngrams(self, query: str):    
        query_tokens = self.vectorizer.build_analyzer()(query)
        print(f"Query n-grams: {query_tokens}")
        matched_chunks = defaultdict(int)

        for ngram in query_tokens:
            for idx in self.inverted_index.get(ngram, []):
                matched_chunks[idx] += 1

        serializable_index = {k: list(v) for k, v in self.inverted_index.items()}

        with open("inverted_index.json", "w") as f:
            json.dump(serializable_index, f, indent=2)

        return sorted(matched_chunks.items(), key=lambda x: -x[1])