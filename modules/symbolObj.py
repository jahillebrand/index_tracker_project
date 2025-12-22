#Import apiObj to process API keys
import api.apiObj as apiObj

# Import Datetime module for grabbing dates
from datetime import datetime, timedelta

# Import REST API features
import requests

# Import time module to handle processing API limits
import time

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


class symbolObj:
    tenThousandDollars=10000
    tooManyRequests=429
    oneHourInSec=(60*60)
    
    
    def __init__(self, symbol):
        self.symbol=symbol
        self.fundName=""
        self.fundStartDate=""
        self.fundEndDate=""
        self.dateLastUpdated=""
        self.lastUpdatedAdjPrice=0.0
        self.lastUpdatedClosePrice=0.0
        self.lastUpdatedSplitFactor=0.0
        self.tenYearAdjPrice=0.0
        self.tenYearClosePrice=0.0
        self.tenYearSplitFactor=0.0
        self.tenYearTenKUsdReturn=0.0
        self.tenYearPctReturn=0.0


    def updateTenYearWDummy(self):
        # Write dummy data out to the object based on passed symbol
        # <Used for testing only>
        self.dateLastUpdated = datetime.now().date()
        self.lastUpdatedAdjPrice = int.from_bytes(
            self.symbol.encode("utf-8"), 
            byteorder="big"
            )
        self.tenYearTenKUsdReturn = self.lastUpdatedAdjPrice * 10 #dummy value
        self.fundName = "AAAAAA"
        self.fundStartDate = "2025-12-31"
        self.fundEndDate = "2025-12-31"


    def updateTenYearWApi(self,apiObj):
        #Update new date
        self.dateLastUpdated = datetime.now().date()
        priorMonthDate = self.dateLastUpdated - timedelta(days=30)
        tenYearPriorDate = priorMonthDate - timedelta(days=10*365)

        # Prepare Header and Parameter Data
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {apiObj.tiingApiKey}'
        }

        # Prior Month Parameters
        priorMonthQueryParameters = {
            "startDate": priorMonthDate,
            "endDate": priorMonthDate,
            "resampleFreq": "monthly",
            "columns": "splitFactor,close,adjClose",
        }

        # Make API call for close price 1 month prior
        priorMonthResponse=self.sendRequest(
            headers,
            priorMonthQueryParameters,
            apiObj.dailyUriBase,
            apiObj.dailyUriSuffix
            )
        self.lastUpdatedAdjPrice = float(priorMonthResponse.json()[0]["adjClose"])
        self.lastUpdatedClosePrice = float(priorMonthResponse.json()[0]["close"])
        self.lastUpdatedSplitFactor = float(priorMonthResponse.json()[0]["splitFactor"])

        # Ten Year Parameters
        tenYearQueryParameters = {
            "startDate": tenYearPriorDate,
            "endDate": priorMonthDate,
            "resampleFreq": "monthly",
            "columns": "splitFactor,close,adjClose",
        }

        # Make API call for 10 years prior
        tenYearResponse=self.sendRequest(
            headers,
            tenYearQueryParameters,
            apiObj.dailyUriBase,
            apiObj.dailyUriSuffix
            )
        self.tenYearAdjPrice = float(tenYearResponse.json()[0]["adjClose"])
        self.tenYearClosePrice = float(tenYearResponse.json()[0]["close"])
        self.tenYearSplitFactor = float(tenYearResponse.json()[0]["splitFactor"])

        # Use close price differences to calculate 10 year return in usd and pct
        # Divide by 0 protection
        if self.tenYearAdjPrice is not 0.0:
            priceRatio = self.lastUpdatedAdjPrice/self.tenYearAdjPrice
        else:
            priceRatio = 0.0
        self.tenYearTenKUsdReturn = symbolObj.tenThousandDollars*priceRatio
        self.tenYearPctReturn = (1-priceRatio)*100

    def updateFundDetails(self,apiObj):
        # Prepare Header and Parameter Data
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {apiObj.tiingApiKey}'
        }

        # Request fund metadata
        metaRequest = self.sendRequest(headers,"",apiObj.dailyUriBase,"")

        # Set fund metadata
        self.fundName = metaRequest.json()['name']
        self.fundStartDate = datetime.strptime(
            metaRequest.json()['startDate'],
            "%Y-%m-%d"
            ).date()
        self.fundStartDate = datetime.strptime(
            metaRequest.json()['endDate'],
            "%Y-%m-%d"
            ).date()  


    def sendRequest(self, requestHeaders, requestQueryParams, uriBase, uriSuffix):
        # Attempt API query, pause, sleep and loop if needed
        while True:
            # Query API
            requestResponse = requests.get(
                f"{uriBase}{self.symbol}{uriSuffix}",
                params=requestQueryParams, 
                headers=requestHeaders
            )

            # Check for Request Limit Exceeded
            if requestResponse.status_code == symbolObj.tooManyRequests:
                # Number of seconds until retry
                retryAfter = requestResponse.headers.get("Retry-After")

                if retryAfter is not None:
                    sleepSeconds = int(retryAfter)
                else:
                    sleepSeconds = symbolObj.oneHourInSec

                sleepWithHeartbeat(sleepSeconds)
                continue

            requestResponse.raise_for_status()
            return requestResponse
    
    

