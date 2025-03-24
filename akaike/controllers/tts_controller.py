from fastapi import APIRouter
from akaike.utils.tts import text_to_speech

router = APIRouter()

@router.post("/speech/")
async def generate_speech(text: str):
    file_path = text_to_speech(text)
    return {"audio_file": file_path}
