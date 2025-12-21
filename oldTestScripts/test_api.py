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

# Send test request to api
# requestResponse = requests.get(t_test_url,
#                               headers=headers)

# VGT test URLs
vgt_name="vgt"
t_daily_url=f"https://api.tiingo.com/tiingo/daily/{vgt_name}/prices"

# Build query param set
query_parameters = {
    "startDate": "2025-11-26",
    "endDate": "2025-11-26",
    "resampleFreq": "daily",
    "columns": "splitFactor,close,adjClose",
}

# Query given above header and params
requestResponse = requests.get(t_daily_url, params=query_parameters, headers=headers)
print(type(requestResponse))

requestResponseJson = requestResponse.json()
print(type(requestResponseJson))

print(requestResponse.json())

adjClose = requestResponseJson[0]["adjClose"]

# Print the response out for validation

print(adjClose)


