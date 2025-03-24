import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
