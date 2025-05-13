from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
#from llama_index.core.tools import FunctionTool
from llama_index.core import PromptTemplate
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import (Settings, VectorStoreIndex, PromptTemplate, get_response_synthesizer)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.llms import ChatMessage
import json
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

from app.prompts import create_system_prompt
from app.helpers.response_helper import extract_think_response

from app.chat_context import ChatContext

index_collection_name = "storage-index-1"
chroma_db_path = "./chroma_db"

embedding_model_name = "all-MiniLM-L6-v2"#"BAAI/bge-small-en-v1.5"
llm_model_name = "qwen3:4b"
similarity_top_k = 10 

def init_llm(): 
    Settings.embed_model = HuggingFaceEmbedding(model_name=embedding_model_name)
    Settings.llm = Ollama(model=llm_model_name, request_timeout=1000.0, base_url = "http://localhost:11446", temperature=0)#, context_window=12000)

def get_ranked_results(question, query_results):
    msgs = []

    for doc in query_results["documents"][0]:
        prompt = f"""Score how well the following paragraph answers the question.

        Question: {question}

        Paragraph: {doc}

        Return only a score from 0 to 10. Do not include the reasoning for the score.

        Only the options listed below are valid answers:
        0
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        """
        p = PromptTemplate(prompt)
        ranking = Settings.llm.predict(p)
        ranking_res = extract_think_response(ranking)
       
        ranking_num = int(ranking_res["content"])

        print(f"THE RANKING Number is {ranking_num}") 

        if int(ranking_num) >= 5:
            msgs.append(doc)
                
    return f"\n".join(msgs)

def predict(ctx: ChatContext):
    question = rewrite_query(ctx.history, ctx.question)

    category = categorize_query(question)

    query_results = query_vector_db(question, category)

    documents = query_results["documents"][0]
    metadatas = query_results["metadatas"][0]

    prompt = None

    for i, metadata in enumerate(metadatas):
        print(f"Comparing {metadata.get("source")} to {category}")
        if metadata and metadata.get("source") == category:
            print("Found matching document:")
            prompt = documents[i]
            break
        
    

    template = create_system_prompt(query_str=question, context_str=prompt)

    res = Settings.llm.predict(PromptTemplate(template))

    response = extract_think_response(res)

    if response["content"] == "NOT FOUND":
        query_results = query_vector_db_by_question(question)
        prompt = get_ranked_results(question, query_results)
        template = create_system_prompt(query_str=question, context_str=prompt)
        res = Settings.llm.predict(PromptTemplate(template))

        return extract_think_response(res)
    
    else:
        return response


def categorize_query(question):
    template = f"""
    You are an assistant capable of categorizing questions by matching a single question to a single category from the following list:
    Early life and career
    Legal career
    Legislative career
    Presidential campaigns
    Presidency (2009–2017)
    Post-presidency (2017–present)
    Cultural and political image
    Legacy and recognition
    Bibliography

    Question: {question}
    
    Respond with just the selected category and nothing more. """

    res = Settings.llm.predict(PromptTemplate(template))

    rewritten = extract_think_response(res)

    print(f"Here is the category {rewritten["content"]}")

    return rewritten["content"]

def rewrite_query(history: list[str], original_query):
    if len(history) < 2:
        return original_query

    template = (
        "Conversation so far:.\n"
        "---------------------\n"
        f"{"\n".join(history)}\n"
        "---------------------\n"
        "Given the previous conversation, "
        "Rewrite the last user question to be self-contained by incorporating necessary context from the conversation."
        "Do not include any assumptions in the response, only a clean, more detailed question."
        "Ensure that the rewritten question does not ask for more information than the original question. "
        "In this context you are Barrack Obama, so any reference to 'you' should be rewritten to address Barrack Obama."
        f"Question: {original_query}\n"
    )

    res = Settings.llm.predict(PromptTemplate(template))

    rewritten = extract_think_response(res)
    
    print(f"DONE REWRITING {original_query} to {res}")

    return rewritten["content"]

def query_vector_db(query, category):
    em = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model_name)
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    collection = chroma_client.get_collection(index_collection_name, embedding_function=em)

    results = collection.query(query_texts=query, where={"source": category})#n_results=similarity_top_k)

    return results


def query_vector_db_by_question(query):
    em = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model_name)
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    collection = chroma_client.get_collection(index_collection_name, embedding_function=em)

    results = collection.query(query_texts=query, n_results=similarity_top_k)

    return results

