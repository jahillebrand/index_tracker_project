from api import apiObj
from modules import listOfSymbols, storedSymbolObj

# Example instantiation
# Create API key and Vanguard Information Technology ETF object
apiKey = apiObj()

# Open csv file, read in names
csvFileName='symbolListFiles/vanguardAdmiralFunds.csv'
jsonFileName="dataFiles/dummySymbolDataFile.json"
pngFileName="exports/dummyPng.png"

vanguardAdmFunds = listOfSymbols(csvFileName)
vanguardAdmFunds.updateAllSymbols(apiKey,True)
vanguardAdmFunds.exportAllSymbolData(jsonFileName)


testDataObj=storedSymbolObj(jsonFileName)
testDataObj.makeTablePng(pngFileName)


