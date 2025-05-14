from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.core import PromptTemplate
from llama_index.core import (Settings, PromptTemplate)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from app.prompts import create_system_prompt, create_ranked_result_prompt, create_categorize_query_prompt, create_rewrite_query_prompt
from app.helpers.response_helper import extract_think_response
from app.dal import query_vector_db_by_question, query_vector_db_by_category, get_metadata, embedding_model_name

from app.chat_context import ChatContext

def init_llm(): 
    Settings.embed_model = HuggingFaceEmbedding(model_name=embedding_model_name)
    Settings.llm = Ollama(model="qwen3", request_timeout=1000.0, base_url = "http://localhost:11446", temperature=0)#, context_window=12000)

def get_ranked_results(question, query_results):
    msgs = []

    for doc in query_results["documents"][0]:
        prompt = create_ranked_result_prompt(question, doc)
        p = PromptTemplate(prompt)
        
        ranking = Settings.llm.predict(p)
        ranking_res = extract_think_response(ranking)
       
        ranking_num = int(ranking_res["content"])

        print(f"THE RANKING Number is {ranking_num}") 

        if ranking_num >= 8:
            return [doc]

        if ranking_num >= 5:
            msgs.append(doc)
                
    return f"\n".join(msgs)

def predict(ctx: ChatContext):
    question = rewrite_query(ctx.history, ctx.question, ctx.wikiPageTitle)

    category = categorize_query(question)

    query_results = query_vector_db_by_category(question, category)

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




