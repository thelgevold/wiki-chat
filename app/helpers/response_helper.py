import re

def extract_think_response(text):
    """
    Extracts context from <think>...</think> tags and the content after </think>.
    
    Args:
        text (str): The input string containing <think> tags and response content.
    
    Returns:
        dict: A dictionary with 'context' and 'content' keys.
    """
    pattern = r"<think>(.*?)</think>\s*(.*)"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        context = match.group(1).strip()
        content = match.group(2).strip()
        if content == "NOT FOUND":
            content = "I am unable to respond to that. Please try to rephrase your question or add more context."
        return {"context": context, "content": content, "role": "Assistant"}
    else:
        return {"context": None, "content": text.strip(), "role": "Assistant"}

