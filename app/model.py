from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.core import PromptTemplate
from llama_index.core import (Settings, PromptTemplate)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from app.prompts import create_system_prompt, create_ranked_result_prompt, create_categorize_query_prompt, create_rewrite_query_prompt
from app.helpers.response_helper import extract_think_response
from app.dal import query_vector_db_by_question, query_vector_db_by_category, get_metadata, embedding_model_name, query_by_ngram

from app.chat_context import ChatContext
 
def init_llm(): 
    Settings.embed_model = HuggingFaceEmbedding(model_name=embedding_model_name)
    Settings.llm = Ollama(model="qwen3:8b", request_timeout=1000.0, base_url = "http://localhost:11446", temperature=0, context_window=6000)

def get_ranked_results(question, query_results):
    msgs = []
  
    for doc in query_results["documents"][0]:
        prompt = create_ranked_result_prompt(question, doc)
        p = PromptTemplate(prompt)
        
        ranking = Settings.llm.predict(p)
        ranking_res = extract_think_response(ranking)
       
        ranking_num = int(ranking_res["content"])

        print(f"THE RANKING Number is {ranking_num}") 

        if ranking_num >= 5:
            msgs.append(doc)
                
    return f"\n".join(msgs)

def predict(ctx: ChatContext):
    question = rewrite_query(ctx.history, ctx.question, ctx.wikiPageTitle)

    category = categorize_query(question)

    query_results = query_vector_db_by_category(question, category)

    documents = query_results["documents"][0]
    metadatas = query_results["metadatas"][0]

    context = None

    for i, metadata in enumerate(metadatas):
        if metadata and metadata.get("source") == category:
            print("Found matching document:")
            context = documents[i]
            break
        
    response = llm_predict(question, context)

    if response["content"] == "NOT FOUND":
        print("Not a good match by category, asking the llm to rank the search documents.")
        query_results = query_vector_db_by_question(question)
        context = get_ranked_results(question, query_results)
        response = llm_predict(question, context)
        
        if response["content"] == "NOT FOUND":
            print("No good search result from vector search. Falling back to ngram search.")
            context = query_by_ngram(question)
            response = llm_predict(question, context)

            if response["content"] == "NOT FOUND":
                response["content"] = "I am unable to respond to that. Please try to rephrase your question or add more context."
    
    return response

def llm_predict(question: str, context: str):
    template = create_system_prompt(query_str=question, context_str=context)
    res = Settings.llm.predict(PromptTemplate(template))

    print(res)

    return extract_think_response(res)

def categorize_query(question):
    categories = get_metadata("source")

    template = create_categorize_query_prompt(question, categories)

    res = Settings.llm.predict(PromptTemplate(template))

    rewritten = extract_think_response(res)

    return rewritten["content"]

def rewrite_query(history: list[str], original_query, title):
    if len(history) < 2:
        return original_query

    template = create_rewrite_query_prompt(history, original_query, title)

    res = Settings.llm.predict(PromptTemplate(template))

    rewritten = extract_think_response(res)
    
    print(f"DONE REWRITING {original_query} to {res}")

    return rewritten["content"]




