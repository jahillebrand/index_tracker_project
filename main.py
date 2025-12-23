from api import apiObj
from modules import listOfSymbols, storedSymbolObj

# Calls all procedures to generate a report
# include full relative path to file
# i.e. 'symbolListFiles/<csvOfTickerNames>.csv'

# TODO: Haven't tested this guy yet, test him in 1 shot after re-writing chart object
def callStockFetcher(inputCsvFilename):
    # Create API key and Vanguard Information Technology ETF object
    apiKey = apiObj()

    # Create fund list from input
    fundList = listOfSymbols(inputCsvFilename)

    # Fetch Fund Data
    fundList.updateAllSymbols(apiKey)

    # Export Fund Data to Storage
    fileArray = inputCsvFilename.replace("/",".").split(".")
    exportFilename = f"datafiles/{fileArray[1]}.json"
    fundList.exportAllSymbolPriceData(exportFilename)



# Example instantiation
# Create API key and Vanguard Information Technology ETF object
apiKey = apiObj()

# Open csv file, read in names
csvFileName='symbolListFiles/vanguardAdmiralFunds.csv'
jsonFileName="dataFiles/newFullDatadump.json"
pngFileName="exports/apiRefactor.png"

vanguardAdmFunds = listOfSymbols(csvFileName)
vanguardAdmFunds.updateAllSymbols(apiKey)
vanguardAdmFunds.exportAllSymbolPriceData(jsonFileName)


#testDataObj=storedSymbolObj(jsonFileName)
#testDataObj.makeTablePng(pngFileName)


