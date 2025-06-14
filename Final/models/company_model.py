from pydantic import BaseModel
from typing import List

class ArticleModel(BaseModel):
    title: str
    summary: str
    sentiment: str
    source: str

class CompanyRequestModel(BaseModel):
    company_name: str

class CompanyResponseModel(BaseModel):
    company: str
    articles: List[ArticleModel]
    comparitive_sentiment: str