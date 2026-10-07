import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

print("API key loaded:", bool(api_key))

url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())
