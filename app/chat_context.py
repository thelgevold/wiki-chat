from pydantic import BaseModel

class ChatContext(BaseModel):
    question: str
    history: list[str]
    wikiPageTitle: str = "Barrack Obama"