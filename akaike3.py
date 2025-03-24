import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os
import streamlit as st
from googletrans import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon (only needed once)
nltk.download('vader_lexicon')

# Initialize session state
if 'news' not in st.session_state:
    st.session_state.news = []

# Scraping function
def scrape_company_news(company_name):
    url = f"https://www.google.com/search?q={company_name}&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve news")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for result in soup.select(".SoaBEf"):
        title = result.select_one(".nDgy9d").text if result.select_one(".nDgy9d") else "No title"
        link = result.a["href"] if result.a else "No link"
        source = result.select_one(".MgUUmf span:last-child").text if result.select_one(".MgUUmf span:last-child") else "Unknown source"
        snippet = result.select_one(".GI74Re.nDgy9d").text if result.select_one(".GI74Re.nDgy9d") else "No content available"

        articles.append({"title": title, "link": link, "source": source, "content": snippet})

    return articles

# Sentiment analysis function using VADER
def analyze_sentiment(text, company_name):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    
    # Determine sentiment based on compound score
    if sentiment_scores['compound'] >= 0.05:
        sentiment = "Positive"
    elif sentiment_scores['compound'] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    # Adjust sentiment based on competition keywords
    competition_keywords = ["competition", "rival", "challenge", "outperform", "overtake", "surpass"]
    if any(keyword in text.lower() for keyword in competition_keywords):
        sentiment = "Negative" if sentiment == "Positive" else sentiment
    
    return sentiment

# Comparative analysis function
def comparative_analysis(articles, company_name):
    sentiments = [analyze_sentiment(article['content'], company_name) for article in articles]
    positive_count = sentiments.count("Positive")
    negative_count = sentiments.count("Negative")
    neutral_count = sentiments.count("Neutral")
    
    st.write(f"Positive: {positive_count}, Negative: {negative_count}, Neutral: {neutral_count}")
    if positive_count > negative_count and positive_count > neutral_count:
        st.write("Overall sentiment is Positive.")
    elif negative_count > positive_count and negative_count > neutral_count:
        st.write("Overall sentiment is Negative.")
    else:
        st.write("Overall sentiment is Neutral.")

# Text-to-speech function
def text_to_speech(text, language='hi'):
    # Translate text to Hindi
    translator = Translator()
    translated = translator.translate(text, dest='hi')
    hindi_text = translated.text
    
    # Convert translated text to speech
    tts = gTTS(text=hindi_text, lang=language)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows
    # os.system("afplay output.mp3")  # For macOS
    # os.system("mpg321 output.mp3")  # For Linux

# Main function for Streamlit UI
def main():
    st.title("News Sentiment Analysis")
    company_name = st.text_input("Enter the company name", "Tesla")
    
    if st.button("Fetch News"):
        st.session_state.news = scrape_company_news(company_name)
    
    if st.session_state.news:
        st.write(f"Fetched {len(st.session_state.news)} articles for {company_name}")
        for article in st.session_state.news:
            st.write(f"Title: {article['title']}")
            st.write(f"Source: {article['source']}")
            st.write(f"Content: {article['content']}")
            sentiment = analyze_sentiment(article['content'], company_name)
            st.write(f"Sentiment: {sentiment}")
        
        comparative_analysis(st.session_state.news, company_name)
        
        if st.button("Convert to Speech"):
            summarized_content = "\n".join([article['content'] for article in st.session_state.news])
            text_to_speech(summarized_content)

if __name__ == "__main__":
    main()
# import requests
# import re
# from bs4 import BeautifulSoup
# from newspaper import Article
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from gtts import gTTS
# import os
# import streamlit as st
# from googletrans import Translator
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import nltk

# # Download VADER lexicon (only needed once)
# nltk.download('vader_lexicon')

# # Initialize session state
# if 'news' not in st.session_state:
#     st.session_state.news = []

# # Function to get valid news URLs
# def get_valid_news_urls(company_name):
#     search_url = f'https://www.google.com/search?q={company_name}+news&tbm=nws'
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     response = requests.get(search_url, headers=headers)
    
#     if response.status_code != 200:
#         print("⚠️ Google News request failed!")
#         return []
    
#     soup = BeautifulSoup(response.text, 'html.parser')
#     links = []
#     for g in soup.find_all('a', href=True):
#         url_match = re.search(r'(https?://\S+)', g['href'])
#         if url_match:
#             url = url_match.group(1).split('&')[0]
#             if "google.com" not in url:
#                 links.append(url)
    
#     return links[:10]  # Limit to top 10 results

# # Function to extract article content
# def extract_article_content(url):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         return article.text
#     except Exception as e:
#         print(f"⚠️ Newspaper3k failed: {e}")
    
#     try:
#         response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         if response.status_code != 200:
#             raise Exception("Request failed")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         paragraphs = soup.find_all('p')
#         return '\n'.join(p.text for p in paragraphs if p.text)
#     except Exception as e:
#         print(f"⚠️ BeautifulSoup failed: {e}")
    
#     try:
#         options = Options()
#         options.add_argument("--headless")
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#         driver.get(url)
#         page_content = driver.page_source
#         driver.quit()
#         soup = BeautifulSoup(page_content, 'html.parser')
#         paragraphs = soup.find_all('p')
#         return '\n'.join(p.text for p in paragraphs if p.text)
#     except Exception as e:
#         print(f"⚠️ Selenium failed: {e}")
    
#     return None

# # Sentiment analysis function using VADER
# def analyze_sentiment(text, company_name):
#     analyzer = SentimentIntensityAnalyzer()
#     sentiment_scores = analyzer.polarity_scores(text)
    
#     # Determine sentiment based on compound score
#     if sentiment_scores['compound'] >= 0.05:
#         sentiment = "Positive"
#     elif sentiment_scores['compound'] <= -0.05:
#         sentiment = "Negative"
#     else:
#         sentiment = "Neutral"
    
#     # Adjust sentiment based on competition keywords
#     competition_keywords = ["competition", "rival", "challenge", "outperform", "overtake", "surpass"]
#     if any(keyword in text.lower() for keyword in competition_keywords):
#         sentiment = "Negative" if sentiment == "Positive" else sentiment
    
#     return sentiment

# # Comparative analysis function
# def comparative_analysis(articles, company_name):
#     sentiments = [analyze_sentiment(article['content'], company_name) for article in articles]
#     positive_count = sentiments.count("Positive")
#     negative_count = sentiments.count("Negative")
#     neutral_count = sentiments.count("Neutral")
    
#     st.write(f"Positive: {positive_count}, Negative: {negative_count}, Neutral: {neutral_count}")
#     if positive_count > negative_count and positive_count > neutral_count:
#         st.write("Overall sentiment is Positive.")
#     elif negative_count > positive_count and negative_count > neutral_count:
#         st.write("Overall sentiment is Negative.")
#     else:
#         st.write("Overall sentiment is Neutral.")

# # Text-to-speech function
# def text_to_speech(text, language='hi'):
#     # Translate text to Hindi
#     translator = Translator()
#     translated = translator.translate(text, dest='hi')
#     hindi_text = translated.text
    
#     # Convert translated text to speech
#     tts = gTTS(text=hindi_text, lang=language)
#     tts.save("output.mp3")
#     os.system("start output.mp3")  # For Windows
#     # os.system("afplay output.mp3")  # For macOS
#     # os.system("mpg321 output.mp3")  # For Linux

# # Main function for Streamlit UI
# def main():
#     st.title("News Sentiment Analysis")
#     company_name = st.text_input("Enter the company name", "Tesla")
    
#     if st.button("Fetch News"):
#         urls = get_valid_news_urls(company_name)
#         articles = []
#         for url in urls:
#             content = extract_article_content(url)
#             if content:
#                 articles.append({"title": "News Article", "content": content})  # Add title if available
        
#         st.session_state.news = articles
    
#     if st.session_state.news:
#         st.write(f"Fetched {len(st.session_state.news)} articles for {company_name}")
#         for article in st.session_state.news:
#             st.write(f"Title: {article['title']}")
#             st.write(f"Content: {article['content'][:500]}...")  # Display first 500 characters
#             sentiment = analyze_sentiment(article['content'], company_name)
#             st.write(f"Sentiment: {sentiment}")
        
#         comparative_analysis(st.session_state.news, company_name)
        
#         if st.button("Convert to Speech"):
#             summarized_content = "\n".join([article['content'] for article in st.session_state.news])
#             text_to_speech(summarized_content)

# if __name__ == "__main__":
#     main()