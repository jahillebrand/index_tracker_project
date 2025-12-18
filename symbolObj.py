#Import apiObj to process API keys
import apiObj

# Import Datetime module for grabbing dates
from datetime import datetime, timedelta

class symbolObj:
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.dateLastUpdated=""
        self.lastUpdatedAdjPrice=0.0
        self.tenYearAnnualReturn=0.0
        self.updateTenYear()

    def updateTenYear(self, apiObj):
        #Update new date
        self.dateLastUpdated = datetime.now().date()
        ten_year_prior_date = self.dateLastUpdated - timedelta(days=10*365)

        # Make API call for close price 1 month prior
        # self.

        # Make API call for 10 years prior

        # Use close price differences to calculate 10 year return
    
    