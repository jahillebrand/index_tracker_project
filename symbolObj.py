#Import apiObj to process API keys
import apiObj

# Import Datetime module for grabbing dates
from datetime import datetime, timedelta

# Import REST API features
import requests

class symbolObj:
    tenThousandDollars=10000
    
    def __init__(self, symbol, apiObj):
        self.symbol = symbol
        self.dateLastUpdated=""
        self.lastUpdatedAdjPrice=0.0
        self.tenYearReturn=0.0
        self.apiObj = apiObj
        self.updateTenYear()

    def updateTenYear(self):
        #Update new date
        self.dateLastUpdated = datetime.now().date()
        priorMonthDate = self.dateLastUpdated - timedelta(days=30)
        tenYearPriorDate = priorMonthDate - timedelta(days=10*365)

        # Make API call for close price 1 month prior
        priorMonthResponse=self.sendRequest(priorMonthDate)
        self.lastUpdatedAdjPrice = float(priorMonthResponse.json()[0]["adjClose"])

        # Make API call for 10 years prior
        tenYearResponse=self.sendRequest(tenYearPriorDate)
        tenYearAdjClose=float(tenYearResponse.json()[0]["adjClose"])

        # Use close price differences to calculate 10 year return
        self.tenYearReturn = self.tenThousandDollars*(self.lastUpdatedAdjPrice/tenYearAdjClose)

    def sendRequest(self, requestDate):
        # Prepare Header Data
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self.apiObj.tiingApiKey}'
        }

        # Prepare params
        query_parameters = {
            "startDate": requestDate,
            "endDate": requestDate,
            "resampleFreq": "monthly",
            "columns": "splitFactor,close,adjClose",
        }

        # Query API
        requestResponse = requests.get(
            f"{self.apiObj.dailyUriBase}{self.symbol}{self.apiObj.dailyUriSuffix}",
            params=query_parameters, 
            headers=headers
        )
        
        return requestResponse
    
    