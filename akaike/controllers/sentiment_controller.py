from fastapi import APIRouter
from akaike.utils.scraper import scrape_company_news
from akaike.utils.sentiment import analyze_sentiment

router = APIRouter()

@router.post("/sentiment/")
async def get_sentiment(text: str):
    return {"sentiment": analyze_sentiment(text)}



@router.get("/comparative/{company_name}")
async def comparative_sentiment(company_name: str):
    articles = scrape_company_news(company_name)
    sentiments = [analyze_sentiment(article["content"]) for article in articles]

    result = {
        "Positive": sentiments.count("Positive"),
        "Negative": sentiments.count("Negative"),
        "Neutral": sentiments.count("Neutral"),
    }
    
    return result
