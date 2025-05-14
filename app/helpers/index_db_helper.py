import chromadb
from chromadb.utils import embedding_functions
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import StorageContext
from llama_index.core import (Settings, VectorStoreIndex, PromptTemplate, get_response_synthesizer)
from llama_index.core.node_parser import TokenTextSplitter

from app.book_service import get_book

from app.article_service import get_article

from sentence_transformers import SentenceTransformer

index_collection_name = "storage-index-1"
chroma_db_path = "./chroma_db"
embedding_model_name = "all-MiniLM-L6-v2"#"BAAI/bge-small-en-v1.5" #"all-MiniLM-L6-v2"

class IndexDBHelper:
    def _create_index(self, chroma_collection):
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection, collection_name=index_collection_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=Settings.embed_model, storage_context=storage_context)

        return index 
 
    def build_index_db(self):
     
        chroma_client = chromadb.PersistentClient(path=chroma_db_path)
      
        if index_collection_name in [c for c in chroma_client.list_collections()]:
            print("Using existing INDEX")
            chroma_collection = chroma_client.get_collection(name=index_collection_name) 
            return self._create_index(chroma_collection)
            #chroma_client.delete_collection(name=index_collection_name)

        sections = get_article("Barack Obama")

        em = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model_name)
        
        chroma_collection = chroma_client.create_collection(name=index_collection_name, embedding_function=em, metadata={"hnsw:space": "cosine"})

        documents = []
        metadatas = []
        ids = [] 

       # token_text_splitter = TokenTextSplitter(chunk_size=5000, chunk_overlap=100)
        
        i = 1
        # for chapter in chapters:
        #     sections = token_text_splitter.split_text(chapter["text"])
        #     for section in sections:
        #         documents.append(section)
        #         metadatas.append({"source": chapter["title"]})
        #         ids.append(str(i))
        #         i = i + 1

            #n pragraphs
       # paragraphs = [p.strip() for p in wiki_text.split('\n\n') if p.strip()]
        #chunks = [paragraphs[i:i+5] for i in range(0, len(paragraphs), 5)]
        #chunk_texts = ['\n\n'.join(chunk) for chunk in chunks][0]
        
        for section in sections:
            if len(section["text"]) > 0:
                documents.append(section["text"])
                metadatas.append({"source": section["title"]})
                i = i + 1
                ids.append(str(i))

                print(section["title"])

            # Single paragraph
            # for p in paragraphs:
            #     if len(p) > 50:
            #         documents.append(p)
            #         metadatas.append({"source": chapter["title"]})
            #         i = i + 1
            #         ids.append(str(i))
        
        chroma_collection.add(
                                documents=documents, 
                                metadatas=metadatas, 
                                ids=ids, 
                                )  
         
        print("Indexing complete")
        return self._create_index(chroma_collection)

    