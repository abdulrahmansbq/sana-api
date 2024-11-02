from pydantic_settings import BaseSettings
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    APP_NAME: str = os.environ.get("APP_NAME")
    WHISPER_DEVICE: str = os.environ.get("WHISPER_DEVICE")
    WHISPER_MODEL: str = os.environ.get("WHISPER_MODEL")
    WATSONX_MODEL_ID: str = os.environ.get("WATSONX_MODEL_ID")
    WATSONX_URL: str = os.environ.get("WATSONX_URL")
    WATSONX_APIKEY: str = os.environ.get("WATSONX_APIKEY")
    WATSONX_PROJECT_ID: str = os.environ.get("WATSONX_PROJECT_ID")
    WATSONX_SPACE_ID: str = os.environ.get("WATSONX_SPACE_ID")
    STORAGE_PATH: str = os.environ.get("STORAGE_PATH")
    PROMPTS_PATH: str = os.environ.get("PROMPTS_PATH")