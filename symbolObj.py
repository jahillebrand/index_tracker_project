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
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.dateLastUpdated=""
        self.lastUpdatedAdjPrice=0.0
        self.tenYearReturn=0.0

    def updateTenYearWDummy(self):
        # Write dummy data out to the object based on passed symbol
        # <Used for testing only>
        self.dateLastUpdated = datetime.now().date()
        self.lastUpdatedAdjPrice = int.from_bytes(
            self.symbol.encode("utf-8"), 
            byteorder="big"
            )
        self.tenYearReturn = self.lastUpdatedAdjPrice * 10 #dummy value

    def updateTenYearWApi(self,apiObj):
        #Update new date
        self.dateLastUpdated = datetime.now().date()
        priorMonthDate = self.dateLastUpdated - timedelta(days=30)
        tenYearPriorDate = priorMonthDate - timedelta(days=10*365)

        # Make API call for close price 1 month prior
        priorMonthResponse=self.sendRequest(priorMonthDate,apiObj)
        self.lastUpdatedAdjPrice = float(priorMonthResponse.json()[0]["adjClose"])

        # Make API call for 10 years prior
        tenYearResponse=self.sendRequest(tenYearPriorDate)
        tenYearAdjClose=float(tenYearResponse.json()[0]["adjClose"])

        # Use close price differences to calculate 10 year return
        self.tenYearReturn = symbolObj.tenThousandDollars*(self.lastUpdatedAdjPrice/tenYearAdjClose)

    def sendRequest(self, requestDate, apiObj):
        # Prepare Header Data
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {apiObj.tiingApiKey}'
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
                f"{apiObj.dailyUriBase}{self.symbol}{apiObj.dailyUriSuffix}",
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