import chromadb
from chromadb.utils import embedding_functions
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import (Settings, VectorStoreIndex)

from app.article_service import get_article
from app.dal import index_collection_name, chroma_db_path, embedding_model_name
from app.helpers.n_gram_helper import NGramHelper

class IndexDBHelper:
    def _create_index(self, chroma_collection):
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection, collection_name=index_collection_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=Settings.embed_model, storage_context=storage_context)

        return index 
 
    def build_index_db(self):
        chroma_client = chromadb.PersistentClient(path=chroma_db_path)
      
        if index_collection_name in [c for c in chroma_client.list_collections()]:
            chroma_collection = chroma_client.get_collection(name=index_collection_name) 
            #return self._create_index(chroma_collection)
            chroma_client.delete_collection(name=index_collection_name)

        sections = get_article("Luke Skywalker")

        text_chunks = [s["text"] for s in sections]
        ngram_helper = NGramHelper()
        ngram_helper.initialize_vectorizer(text_chunks)
        

        em = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model_name)
        
        chroma_collection = chroma_client.create_collection(name=index_collection_name, embedding_function=em, metadata={"hnsw:space": "cosine"})

        documents = []
        metadatas = []
        ids = [] 
 
        i = 1
        
        for section in sections:
            if len(section["text"]) > 0:
                documents.append(section["text"])
                metadatas.append({"source": section["title"]})
                
                ngram_helper.add_to_inverted_index(section["text"], i)
                ids.append(str(i))

                i = i + 1

        chroma_collection.add(
                                documents=documents, 
                                metadatas=metadatas, 
                                ids=ids, 
                                )  
         
        print("Indexing complete")
        return self._create_index(chroma_collection)

    