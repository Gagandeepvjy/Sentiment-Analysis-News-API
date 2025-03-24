import requests
import streamlit as st

FASTAPI_URL = "http://localhost:8000/api"

if 'news' not in st.session_state:
    st.session_state.news = []
    st.session_state.comparitive_sentiment = ""


def fetch_news(company_name):
    try:
        response = requests.get(f"{FASTAPI_URL}/news/{company_name}")
        data = response.json()
        if data["status_code"] == 200:
            return data["data"], None
        else:
            return [], data["error"]
    except Exception as e:
        return [], str(e)



def text_to_speech(company_name):
    try:
        body = {
            "company_name":company_name
        }
        response = requests.post(f"{FASTAPI_URL}/speech/", json = body)
        data = response.json()
        if data["status_code"] == 201:
            st.success("Text-to-Speech generated successfully! Check your audio output.")
        else:
            st.error(f"Error in Text-to-Speech: {data['error']}")
    except Exception as e:
        st.error(f"Exception occurred: {str(e)}")


def main():
    st.title("News Sentiment Analysis using FastAPI")
    company_name = st.text_input("Enter the company name", "Tesla")

    if st.button("Fetch News"):
        data, error = fetch_news(company_name)

        if error:
            st.error(f"Error fetching news: {error}")
        else:
            st.session_state.news = data["articles"]
            st.session_state.comparitive_sentiment = data["comparitive_sentiment"]

    if st.session_state.news:
        st.write(f"### News articles for **{company_name}**")
        
        
        for article in st.session_state.news:
            st.write(f"#### {article['title']}")
            st.write(f"**Source:** {article['source']}")
            st.write(f"**Content:** {article['summary']}")
            st.write(f"**Sentiment:** {article.get('sentiment', 'N/A')}")
            st.markdown(f"[🔗 Read more]({article['source']})", unsafe_allow_html=True)
            st.write("---")

        st.write(f"### Comparitive Sentiment: **{st.session_state.comparitive_sentiment}**")
        st.write("---")     
        if st.button("🔊 Convert to Speech"):
            text_to_speech(company_name)


if __name__ == "__main__":
    main()
