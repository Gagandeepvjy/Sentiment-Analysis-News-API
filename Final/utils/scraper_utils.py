import requests
from typing import Optional, List
from bs4 import BeautifulSoup
from akaike.models import ArticleModel
from .sentiment_utils import analyze_sentiment
def scrape_company_news(company_name) -> tuple[Optional[List[ArticleModel]],Optional[str]]:
    try:
        url = f"https://www.google.com/search?q={company_name}&tbm=nws"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {"error": "Failed to retrieve news"}

        soup = BeautifulSoup(response.text, "html.parser")
        articles = []

        for result in soup.select(".SoaBEf"):
            title = result.select_one(".nDgy9d").text if result.select_one(".nDgy9d") else "No title"
            link = result.a["href"] if result.a else "No link"
            source = result.select_one(".MgUUmf span:last-child").text if result.select_one(".MgUUmf span:last-child") else "Unknown source"
            snippet = result.select_one(".GI74Re.nDgy9d").text if result.select_one(".GI74Re.nDgy9d") else "No content available"
            sentiment, error = analyze_sentiment(snippet)
            if error:
                return None, error
            data = {"title": title, "source": source, "summary": snippet,"sentiment": sentiment}
            articles.append(ArticleModel(**data))

        return articles, None
    except Exception as e:
        return None, str(e)
