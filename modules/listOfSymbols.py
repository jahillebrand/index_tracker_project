# Import os to handle file reads/writes
import os
# Import csv and json to handle import/export
import csv
import json
# Import symbolObj to handle symbolObjects
from .symbolObj import symbolObj
# Import Pathlib to handle path management for json filewrites
from pathlib import Path

# Function to append new data to JSON file
import json

""" # Helper function to write data out (append) to a specified json file
def writeJson(newData, filename, dataKey):
    with open(filename, "a+") as file:
        file.seek(0)

        try:
            file_data = json.load(file)
        except json.JSONDecodeError:
            # File is empty or corrupted — initialize it
             file_data = {
                dataKey: []
            } 
            file_data[dataKey] = {}

        # Append new data
        #file_data[dataKey].append(newData)
        print(file_data)
        print(dataKey)
        file_data[dataKey].update(newData)

        # Rewrite file clean
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4) """

# Helper function to write out json files
def writeJson(newData, filename, dataKey):
    print(f"Now writing out: {dataKey}")
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

    # Step 2: Add or overwrite the key
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
            "fundStartDate" : symbolObj.fundStartDate,
            "fundEndDate" : symbolObj.fundEndDate,
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
        if os.path.exists(f"{baseJsonFilename}.json"):
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
                    pass
                    # TODO: Need a loader function so the object can load in its metadata

        # If we fetched metadata, dump it out so we don't need it next time


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
                    "tenYearAdjPrice" : str(symbolObj.tenYearAdjPrice),
                    "tenYearClosePrice" : str(symbolObj.tenYearClosePrice),
                    "tenYearSplitFactor" : str(symbolObj.tenYearSplitFactor),
                    "tenYearTenKUsdReturn" : str(symbolObj.tenYearTenKUsdReturn),
                    "tenYearPctReturn" : str(symbolObj.tenYearPctReturn)
                }

                # Write it out
                writeJson(symbolDataToWrite,outputFilename,symbolObj.symbol)
        
        #else if other filetype, add logic here

    # Helper function to unpack and assign data 
    # TODO: Half-baked, get this working later
    def loadExistingMetaData(self,fileName):
        # Get file path name
        filePath = Path(fileName)

        # Open the file, read the json data
        with filePath.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Traverse the object list, populate with the symbol metadata
        for symbolObj in self.symbolObjList:
            symbolObj.fundName = data.get(symbolObj.symbol).get("fundName")
            symbolObj.fundStartDate = data.get(symbolObj.symbol).get("fundStartDate")
            symbolObj.fundEndDate = data.get(symbolObj.symbol).get("fundEndDate")


    




