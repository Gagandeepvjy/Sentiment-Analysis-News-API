from pydantic import BaseModel


class SentimentRequestModel(BaseModel):
    text: str
    company_name: str