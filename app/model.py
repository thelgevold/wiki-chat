from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
#from llama_index.core.tools import FunctionTool
from llama_index.core import PromptTemplate

llm_model_name = "qwen3"

def init_llm(): 
    Settings.llm = Ollama(model=llm_model_name, request_timeout=1000.0, base_url = "http://localhost:11434", temperature=0, context_window=10000)

def predict(prompt: str):
    return Settings.llm.predict(prompt=PromptTemplate(prompt))

# def predict(title: str):
#     article = get_article(title=title)
        
#     tool = FunctionTool.from_defaults(fn=get_country_border_info, name="get_country_border_info")
   
#     prompt = f"Get information about {title} based on {article}. Rely only on the provided document when generating the response"

#     res = Settings.llm.predict_and_call([tool], prompt, verbose = True)
  
#     return res.response