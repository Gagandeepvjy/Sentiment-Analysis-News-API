import nltk
from typing import List
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from akaike.models.company_model import ArticleModel

nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    try:
        sentiment_scores = analyzer.polarity_scores(text)
        if sentiment_scores["compound"] >= 0.05:
            return "Positive",None
        elif sentiment_scores["compound"] <= -0.05:
            return "Negative",None
        return "Neutral",None
    except Exception as e:
        return None, str(e)

def bulk_analyze_sentiment(articles: List[ArticleModel]):
    results = []
    for article in articles:
        sentiment, error = analyze_sentiment(article.summary)
        if error:
            return None,error
        results.append(sentiment)
    return results, None