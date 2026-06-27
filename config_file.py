from dotenv import load_dotenv
import os

load_dotenv()
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")



