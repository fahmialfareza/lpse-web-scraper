from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Access environment variables
LPSE_URL = os.getenv("LPSE_URL")
LPSE_AUTHENTICITY_TOKEN = os.getenv("LPSE_AUTHENTICITY_TOKEN")
LPSE_COOKIE = os.getenv("LPSE_COOKIE")
LPSE_USER_AGENT = os.getenv("LPSE_USER_AGENT")
LPSE_LELANG_DATA_LENGTH = os.getenv("LPSE_LELANG_DATA_LENGTH")
