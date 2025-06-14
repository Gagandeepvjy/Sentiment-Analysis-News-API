"""
FastAPI Application Initialization

This script sets up the FastAPI app, configures settings,
and imports required modules (models, views, and routes).
"""

import os
from fastapi import FastAPI
from .controllers import news_controller, sentiment_controller, text_to_speech_controller
from fastapi.middleware.cors import CORSMiddleware
SECRET_KEY = os.urandom(32)

app = FastAPI(title = "Akaike Technology - News Sentiment Analysis API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(news_controller.router, prefix="/api", tags=["News"])
app.include_router(sentiment_controller.router, prefix="/api", tags=["Sentiment"])
app.include_router(text_to_speech_controller.router, prefix="/api", tags=["Speech"])



