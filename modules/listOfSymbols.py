# Import csv and json to handle import/export
import csv
import json
# Import symbolObj to handle symbolObjects
from .symbolObj import symbolObj

# Function to append new data to JSON file
import json

def writeJson(newData, filename):
    with open(filename, "a+") as file:
        file.seek(0)

        try:
            file_data = json.load(file)
        except json.JSONDecodeError:
            # File is empty or corrupted — initialize it
            file_data = {
                "symbolData": []
            }

        # Append new data
        file_data["symbolData"].append(newData)

        # Rewrite file clean
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)



class listOfSymbols:
    def __init__(self,inputFilename,type="csv"):
        # Initialize data, if statement to call file import function
        self.inputFilename = inputFilename
        self.symbolNamesList = []
        self.symbolObjList = []

        # Check filetype, perform import
        if type == "csv":
            self.importCsvSymbolList(self.inputFilename)
        #else if other filetype, add logic here


    def importCsvSymbolList(self,filename,clear=True):
        # Clear symbol list if it has stale data in it
        if clear:
            self.symbolNamesList=[]

        # Open the csv file, read in the names
        with open(filename, mode='r')as file:
            csvFileHandler=csv.reader(file)
            # Drop file lines into a list for easier processing
            for lines in csvFileHandler:
                self.symbolNamesList = self.symbolNamesList+lines

        # Generate Objects for each symbol
        for symbol in self.symbolNamesList:
            tempObj = symbolObj(symbol.lower())
            self.symbolObjList.append(tempObj)
        

    def updateAllSymbols(self, apiObj, withDummyVals=False):
        # Call the given API to update all symbols with required data
        #for symbol in self.symbolNamesList:
        if withDummyVals == True:
            for symbolObj in self.symbolObjList:
                symbolObj.updateTenYearWDummy()
        else:
            for symbolObj in self.symbolObjList:
                symbolObj.updateTenYearWApi(apiObj)


    def exportAllSymbolData(self,outputFilename='symbolDataFile.json', type="json"):
        if type == "json":
            # Iterate through all symbol objects, export them 1 at a time into the json file
            for symbolObj in self.symbolObjList:

                # Pack data for Json write
                symbolDataToWrite = {
                    "symbol" : symbolObj.symbol,
                    "dateLastupdated" : str(symbolObj.dateLastUpdated),
                    "lastUpdatedAdjPrice" : str(symbolObj.lastUpdatedAdjPrice),
                    "tenYearReturn" : str(symbolObj.tenYearReturn),
                }

                # Write it out
                writeJson(symbolDataToWrite,outputFilename)
        
        #else if other filetype, add logic here



