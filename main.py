from api import apiObj
from modules import listOfSymbols, storedSymbolObj
from datetime import datetime

# Calls all procedures to generate a report
# include full relative path to file
# i.e. 'symbolListFiles/<csvOfTickerNames>.csv'
def callStockFetcher(inputCsvFilename):
    # Get the date
    todaysDate = str(datetime.now().date())

    # Create API key and Vanguard Information Technology ETF object
    apiKey = apiObj()

    # Create fund list from input
    fundList = listOfSymbols(inputCsvFilename)

    # Fetch Fund Data
    fundList.updateAllSymbols(apiKey)

    # Export Fund Data to Storage
    fileArray = inputCsvFilename.replace("/",".").split(".")
    dataExportFilename = f"datafiles/{todaysDate}_{fileArray[1]}.json"
    fundList.exportAllSymbolPriceData(dataExportFilename)

    # Load the Stored Data, and generate a report
    testDataObj=storedSymbolObj(dataExportFilename)
    testDataObj.makeTablePdf()


# csvFileToProcess
csvFileName='symbolListFiles/vanguardAdmiralFunds.csv'
callStockFetcher(csvFileName)



