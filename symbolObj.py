#Import apiObj to process API keys
import apiObj

# Import Datetime module for grabbing dates
from datetime import datetime, timedelta

# Import REST API features
import requests

# Import time module to handle processing API limits
import time

class symbolObj:
    tenThousandDollars=10000
    tooManyRequests=429
    oneHourInSec=(60*60)
    
    def __init__(self, symbol, apiObj):
        self.symbol = symbol
        self.dateLastUpdated=""
        self.lastUpdatedAdjPrice=0.0
        self.tenYearReturn=0.0
        self.apiObj = apiObj
        #self.updateTenYear()

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
        self.tenYearReturn = symbolObj.tenThousandDollars*(self.lastUpdatedAdjPrice/tenYearAdjClose)

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

        # Attempt API query, pause, sleep and loop if needed
        while True:
            # Query API
            requestResponse = requests.get(
                f"{self.apiObj.dailyUriBase}{self.symbol}{self.apiObj.dailyUriSuffix}",
                params=query_parameters, 
                headers=headers
            )

            # Check for Request Limit Exceeded
            if requestResponse.status_code == symbolObj.tooManyRequests:
                # Number of seconds until retry
                retryAfter = requestResponse.headers.get("Retry-After")

                if retryAfter is not None:
                    sleepSeconds = int(retryAfter)
                else:
                    sleepSeconds = symbolObj.oneHourInSec

                self.sleepWithHeartbeat(sleepSeconds)
                continue

            requestResponse.raise_for_status()
            return requestResponse
    
    def sleepWithHeartbeat(totalSeconds, interval=30):
        # Grab remaining seconds
        remaining = totalSeconds

        # Begin looping time printouts
        while remaining > 0:
            mins, secs = divmod(remaining, 60)
            print(
                f"\rRate limited — retrying in {mins:02d}:{secs:02d} ",
                end="",
                flush=True
            )

            sleepTime = min(interval, remaining)
            time.sleep(sleepTime)
            remaining -= sleepTime

        print("\rRetrying now...            ")
    