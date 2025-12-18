# Import OS features
import os 
# Import dotenv functionality
from dotenv import load_dotenv, dotenv_values
# Import REST API features
import requests

# load .env file
load_dotenv()

# Load API key
key="TIING_API_KEY"
t_api_key = os.environ.get(key,None)
if t_api_key is None:
    raise ValueError(f"Required environment variable '{key}' is not set")

# Uncomment to validate API key
# print(f"APIKey: {t_api_key}")

# TIING Test URL
t_test_url="https://api.tiingo.com/api/test/"

# Pack request header
headers = {

        'Content-Type': 'application/json',
        'Authorization': f'Token {t_api_key}'
}

requestResponse = requests.get(t_test_url,
                               headers=headers)

print(requestResponse.json())


