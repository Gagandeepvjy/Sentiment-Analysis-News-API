from fastapi import APIRouter, status
from akaike.utils.scraper import scrape_company_news
from akaike.utils.sentiment import analyze_sentiment, bulk_analyze_sentiment
from akaike.models.response_model import ResponseBaseModel
router = APIRouter()

@router.post("/sentiment/")
async def get_sentiment(text: str):
    return {"sentiment": analyze_sentiment(text)}



@router.get("/comparative/{company_name}")
async def comparative_sentiment(company_name: str):
    articles,error = scrape_company_news(company_name)
    if error:
        return ResponseBaseModel(
            data = None,
            error = error,
            message = "Error Processing Request",
            status_code = status.HTTP_400_BAD_REQUEST

        )
    sentiments, error = bulk_analyze_sentiment(articles)
    if error:
        return ResponseBaseModel(
            data = None,
            error = error,
            message = "Error Processing Request",
            status_code = status.HTTP_400_BAD_REQUEST

        )
    result = {
        "Positive": sentiments.count("Positive"),
        "Negative": sentiments.count("Negative"),
        "Neutral": sentiments.count("Neutral"),
    }
    
    return ResponseBaseModel(
        data = result,
        error = None,
        message = "Successfully Analysed Data",
        status_code = status.HTTP_200_OK
    )
