from apiObj import apiObj
from symbolObj import symbolObj

import csv

import json

# Function to append new data to JSON file
def write_json(new_data, filename='symbolDataFile.json'):
    with open(filename, 'r+') as file:
        # Load existing data into a dictionary
        file_data = json.load(file)
        
        # Append new data to the 'emp_details' list
        file_data["symbolData"].append(new_data)
        
        # Move the cursor to the beginning of the file
        file.seek(0)
        
        # Write the updated data back to the file
        json.dump(file_data, file, indent=4)


# Example instantiation
# Create API key and Vanguard Information Technology ETF object
#apiKey = apiObj()
#vgtObj = symbolObj("vgt",apiKey)

# Print Results
#print(vgtObj.lastUpdatedAdjPrice)
#print(vgtObj.tenYearReturn)
csvFileContents=[]
parsedSymbolList=[]

# Open csv file, read in names
csvFileName='symbolsList.csv'
with open(csvFileName, mode='r')as file:
    csvFileHandler=csv.reader(file)
    for lines in csvFileHandler:
        csvFileContents = csvFileContents+lines

# Drop symbols to all lowercase
for line in range(len(csvFileContents)):
    parsedSymbolList.append(csvFileContents[line].lower())

# Max 37. This gets run manually currently
# TODO: Make this run in a loop, which pauses every 20 symbols to allow API cooldown time
evalPosition=37
print(f"Now evaluating: {parsedSymbolList[evalPosition]}")

# Create API key and generic symbol object
apiKey = apiObj()
genericSymbolObj = symbolObj(parsedSymbolList[evalPosition],apiKey)

# Print Results
print(genericSymbolObj.lastUpdatedAdjPrice)
print(genericSymbolObj.tenYearReturn)

# Pack data for Json write
symbolDataToWrite = {
    "symbol" : genericSymbolObj.symbol,
    "dateLastupdated" : str(genericSymbolObj.dateLastUpdated),
    "lastUpdatedAdjPrice" : str(genericSymbolObj.lastUpdatedAdjPrice),
    "tenYearReturn" : str(genericSymbolObj.tenYearReturn),
}

write_json(symbolDataToWrite)

