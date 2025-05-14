from chromadb.utils import embedding_functions
import chromadb

chroma_db_path = "./chroma_db"
similarity_top_k = 10
index_collection_name = "storage-index-1"
embedding_model_name = "all-MiniLM-L6-v2"#"BAAI/bge-small-en-v1.5"

def query_vector_db_by_category(query, category):
    em = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model_name)
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    collection = chroma_client.get_collection(index_collection_name, embedding_function=em)

    results = collection.query(query_texts=query, where={"source": category})

    return results


def query_vector_db_by_question(query):
    em = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model_name)
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    collection = chroma_client.get_collection(index_collection_name, embedding_function=em)

    results = collection.query(query_texts=query, n_results=similarity_top_k, include=["distances", "metadatas", "documents"])

    distances = results["distances"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    sorted_items = sorted(zip(distances, documents, metadatas), key=lambda x: x[0])

    # Reconstruct the original return format
    sorted_results = {
        "documents": [[doc for _, doc, _ in sorted_items]],
        "metadatas": [[meta for _, _, meta in sorted_items]],
        "distances": [[dist for dist, _, _ in sorted_items]]
    }

    return sorted_results