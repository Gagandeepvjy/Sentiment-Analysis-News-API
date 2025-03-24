from fastapi import APIRouter, Depends, status
from akaike.utils.text_to_speech_utils import text_to_speech
from akaike.utils.scraper_utils import scrape_company_news
from akaike.models.company_model import CompanyRequestModel
from akaike.models.response_model import ResponseBaseModel

router = APIRouter()

@router.post("/speech/")
async def generate_speech(request: CompanyRequestModel = Depends()):
    articles, error = scrape_company_news(request.company_name)
    if error:
        return ResponseBaseModel(
            data  = None,
            error = error,
            message = "Error Processing Request",
            status_code = status.HTTP_400_REQUEST
        )
    file_path, error = text_to_speech(articles)
    if error:
        return ResponseBaseModel(
            data = None,
            error = error,
            message = "Error Processing Request",
            status_code = status.HTTP_400_REQUEST
        )
    return ResponseBaseModel(
        data = file_path,
        error = None,
        message = "Successfully converted text to speech",
        status_code = status.HTTP_201_CREATED
    )
