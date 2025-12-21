# Import OS features
import os 
# Import dotenv functionality
from dotenv import load_dotenv, dotenv_values

# load .env file
load_dotenv()

class apiObj:
    def __init__(self):
        # Load API key
        key="TIING_API_KEY"
        self.tiingApiKey = os.environ.get(key,None)
        if self.tiingApiKey is None:
            raise ValueError(f"Required environment variable '{key}' is not set")
        
        # Define TIING URIs for queries
        self.testUri = "https://api.tiingo.com/api/test/"
        self.dailyUriBase = "https://api.tiingo.com/tiingo/daily/"
        self.dailyUriSuffix = "/prices"