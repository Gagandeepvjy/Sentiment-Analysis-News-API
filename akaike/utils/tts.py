from gtts import gTTS
import os
from googletrans import Translator

def text_to_speech(text, language="hi"):
    translator = Translator()
    translated = translator.translate(text, dest=language).text
    tts = gTTS(text=translated, lang=language)
    output_path = "output.mp3"
    tts.save(output_path)
    return output_path
