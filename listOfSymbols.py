import csv

class listOfSymbols:
    pass

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
        

    def updateAllSymbols(self, apiObj):
        # Call the given API to update all symbols with required data
        #for symbol in self.symbolNamesList:

        pass

    def exportAllSymbolData(self,outputFilename):
        pass
