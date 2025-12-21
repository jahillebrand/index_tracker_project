import csv
from symbolObj import symbolObj

class listOfSymbols:


    def __init__(self,inputFilename,type="csv"):
        # Initialize data, if statement to call file import function
        self.inputFilename = inputFilename
        self.symbolNamesList = []
        self.symbolObjList = []

        # Check filetype, perform import
        if type == "csv":
            self.importCsvSymbolList(self.inputFilename)


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


    def exportAllSymbolData(self,outputFilename):
        pass
