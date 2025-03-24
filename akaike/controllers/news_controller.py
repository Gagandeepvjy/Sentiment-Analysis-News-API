from fastapi import APIRouter, Depends, status
from akaike.utils.scraper_utils import scrape_company_news
from akaike.models.company_model import CompanyRequestModel, CompanyResponseModel
from akaike.models.response_model import ResponseBaseModel

router = APIRouter()

@router.get("/news/{company_name}")
async def get_news(request: CompanyRequestModel = Depends()):
    scrapped_data, error = scrape_company_news(request.company_name)

    if error:
        response = ResponseBaseModel(
            data=None,
            error=error,
            message="News Scraped Unsuccessfully",
            status_code=status.HTTP_400_BAD_REQUEST
        )
        return response.model_dump()

    company_response = CompanyResponseModel(
        company=request.company_name,
        articles=scrapped_data
    )

    response = ResponseBaseModel(
        data=company_response,
        error=None,
        message="News Scraped Successfully",
        status_code=status.HTTP_200_OK
    )

    return response

