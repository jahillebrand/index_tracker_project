# Import os to handle file reads/writes
import os
# Import csv and json to handle import/export
import csv
import json
# Import datetime to process dates
from datetime import datetime
# Import symbolObj to handle symbolObjects
from .symbolObj import symbolObj
# Import Pathlib to handle path management for json filewrites
from pathlib import Path

# Function to append new data to JSON file
import json

# Helper function to write out json files
def writeJson(newData, filename, dataKey):
    filePath = Path(filename)

    # Step 1: Load existing data or start fresh
    if filePath.exists():
        with filePath.open("r", encoding="utf-8") as f:
            try:
                fileData = json.load(f)
            except json.JSONDecodeError:
                # File exists but is empty or corrupted
                fileData = {}
    else:
        fileData = {}

    # Step 2: Add or overwrite the dataKey
    fileData[dataKey] = newData

    # Step 3: Write everything back to disk
    with filePath.open("w", encoding="utf-8") as f:
        json.dump(fileData, f, indent=2)



# Helper function to pack symbolObj meta data for write out to a json file
# NOTE: CALL ONLY ON SINGLE symbolObj, NOT listOfSymbols
def exportSymbolMetaData(symbolObj, baseFilename, type="json"):
    if type == "json":
        # Build the filename, pack the data
        exportFilename = f"{baseFilename}.json"
        symbolDataToWrite = {
            "fundName" : symbolObj.fundName,
            "fundStartDate" : str(symbolObj.fundStartDate),
            "fundEndDate" : str(symbolObj.fundEndDate),
        }

        # Write it out
        writeJson(symbolDataToWrite,exportFilename,symbolObj.symbol)

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
        # Check if separate file exists with basic fund metadata
        needMetaData=True
        baseJsonFilename, _ = os.path.splitext(self.inputFilename)
        jsonFilename = f"{baseJsonFilename}.json"
        if os.path.exists(jsonFilename):
            needMetaData=False

        # Call the given API to update all symbols with required data
        #for symbol in self.symbolNamesList:
        if withDummyVals == True:
            for symbolObj in self.symbolObjList:
                symbolObj.updateTenYearWDummy()
                exportSymbolMetaData(symbolObj,baseJsonFilename)
        else:
            for symbolObj in self.symbolObjList:
                symbolObj.updateTenYearWApi(apiObj)
                if needMetaData: # Fetch metadata, and export it for future use (saves API b/w)
                    symbolObj.updateFundDetails(apiObj)
                    exportSymbolMetaData(symbolObj,baseJsonFilename)
                else:
                    self.loadExistingMetaData(jsonFilename)


    def exportAllSymbolPriceData(self,outputFilename='symbolDataFile.json', type="json"):
        if type == "json":
            # Iterate through all symbol objects, export them 1 at a time into the json file
            for symbolObj in self.symbolObjList:

                # Pack data for Json write
                symbolDataToWrite = {
                    "symbol" : symbolObj.symbol,
                    "dateLastupdated" : str(symbolObj.dateLastUpdated),
                    "lastUpdatedAdjPrice" : str(symbolObj.lastUpdatedAdjPrice),
                    "lastUpdatedClosePrice" : str(symbolObj.lastUpdatedClosePrice),
                    "lastUpdatedSplitFactor" : str(symbolObj.lastUpdatedSplitFactor),
                    "tenYearDate" : str(symbolObj.tenYearDate),
                    "tenYearAdjPrice" : str(symbolObj.tenYearAdjPrice),
                    "tenYearClosePrice" : str(symbolObj.tenYearClosePrice),
                    "tenYearSplitFactor" : str(symbolObj.tenYearSplitFactor),
                    "tenYearTenKUsdReturn" : str(symbolObj.tenYearTenKUsdReturn),
                    "tenYearCagr" : str(symbolObj.tenYearCagr)
                }

                # Write it out
                writeJson(symbolDataToWrite,outputFilename,symbolObj.symbol)
        
        #else if other filetype, add logic here

    # Helper function to unpack and assign data 
    def loadExistingMetaData(self,fileName):
        # Get file path name
        filePath = Path(fileName)

        # Open the file, read the json data
        with filePath.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Traverse the object list, populate with the symbol metadata
        for symbolObj in self.symbolObjList:
            symbolObj.fundName = data.get(symbolObj.symbol).get("fundName")
            # Find dates, convert them to datetime.date() objects
            startDateStr = data.get(symbolObj.symbol).get("fundStartDate")
            endDateStr = data.get(symbolObj.symbol).get("fundEndDate")
            symbolObj.fundStartDate = datetime.strptime(startDateStr,"%Y-%m-%d").date()
            symbolObj.fundEndDate = datetime.strptime(endDateStr,"%Y-%m-%d").date()


    




