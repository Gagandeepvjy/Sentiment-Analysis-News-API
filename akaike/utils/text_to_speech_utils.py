from gtts import gTTS
import os
from typing import List
from akaike.models.company_model import ArticleModel
from googletrans import Translator

def text_to_speech(articles: List[ArticleModel], language: str="hi"):
    try:
        summarized_content = "\n".join([article.summary for article in articles])
        translator = Translator()

        translated = translator.translate(summarized_content, dest=language).text
        tts = gTTS(text=translated, lang=language)
        output_path = "output.mp3"
        tts.save(output_path)
        return output_path, None
    except Exception as e:
        return None, str(e)
