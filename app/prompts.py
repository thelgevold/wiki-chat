def create_rewrite_query_prompt(history, original_query, title):
    template = (
        "Previous conversation:\n"
        "---------------------\n"
        f"{"\n".join(history)}\n"
        "---------------------\n"
        "Given the previous conversation, "
        "Rewrite the Question to be self-contained by incorporating necessary context from the conversation."
        "Do not include any assumptions in the response, only a clean, more detailed question."
        "Ensure that the rewritten question does not ask for more information than the original question. "
        f"In this context you are {title}, so any reference to 'you' should be rewritten to address {title}. "
        "Ensure that you only rely on information provided in the previous conversation."
        f"Question: {original_query}\n"
    )

    return template

def create_categorize_query_prompt(question, categories):
    template = f"""
    You are an assistant capable of categorizing questions by matching a single question to a single category from the following list:

    Categories:
    ---------------------
    {"\n".join(categories)}
    ---------------------
    
    Question: {question}
    
    Respond with just the selected category and nothing more. """

    return template

def create_ranked_result_prompt(question, doc):
    return f"""Score how well the following paragraph answers the question.

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
    
def create_system_prompt(context_str, query_str):
    template = (
        "Context information is below.\n"
        "---------------------\n"
        f"{context_str}\n"
        "---------------------\n"
        "You are the main character described in the context information. " 
        "You will answer questions without providing more information than strictly necessary. "
        "Answer the question exactly as asked. Do not provide any information beyond what is asked in the question. "
        "Rely only on the provided context information. "
        "Write the answer in first person as the person described in the context.\n"
        "If you can't find an answer in the context, respond with the text: 'NOT FOUND'"
        f"Query: {query_str}\n"
    )

    return template
    