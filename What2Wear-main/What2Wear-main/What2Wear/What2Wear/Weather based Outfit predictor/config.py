import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Put your key in .env
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

