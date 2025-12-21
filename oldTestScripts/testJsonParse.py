import json

from storedSymbolObj import storedSymbolObj

import matplotlib.pyplot as plt

# ChatGPT gave me this to make a png
def makeTablePng(dataList, outputPath):
    # Build the table row-by-row, top to bottom
    # Easy, readable, and does exactly what we want
    tableData = []

    for rowDict in dataList:
        # Symbols should always look sharp — uppercase cleans it up
        symbolValue = str(rowDict["symbol"]).upper()

        # Format the 10-year return like real money:
        # dollar sign, commas, and two clean decimals
        tenYearValue = rowDict["tenYearReturn"]
        formattedReturn = f"${float(tenYearValue):,.2f}"

        tableData.append([symbolValue, formattedReturn])

    # Column headers — short, clear, and professional
    columnLabels = ["Symbol", "10-Year Return"]
    # Figure size scales with number of rows so nothing feels cramped
    fig, ax = plt.subplots(figsize=(6, len(tableData) * 0.35))
    ax.axis("off")  # No axes, no noise — just the table

    # Drop the table right into the figure
    table = ax.table(
        cellText=tableData,
        colLabels=columnLabels,
        loc="center",
        cellLoc="left"
    )

    # Font tuning so it looks clean and readable
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.2)

    # Style tweaks: bold headers and right-align the money column
    for (rowIndex, colIndex), cell in table.get_celld().items():
        if rowIndex == 0:
            cell.set_text_props(weight="bold")
        if colIndex == 1 and rowIndex != 0:
            cell.set_text_props(ha="right")

    # Save it out crisp and print-ready
    plt.savefig(outputPath, bbox_inches="tight", dpi=200)
    plt.close(fig)



""" Old procedural logic, testing class logic below
# Read the stored Json file
with open('symbolDataFile.json', 'r') as file:
    testJsonData=json.load(file)

# Initialize list, and copy in file contents
tickerDataList=[]
for line in testJsonData['symbolData']:
    tickerDataList.append(line)

# Sort this list by 10 year returns, largest to smallest
sortedTickerDataList=sorted(tickerDataList, key=lambda d: d['tenYearReturn'], reverse=True)

# Do something with this information
print(sortedTickerDataList)

# Make a little png
makeTablePng(
    dataList=sortedTickerDataList,
    outputPath="tenYearReturn.png"
) """

testDataFilename="symbolDataFile.json"
outputFilename="testTenYearReturn.png"
testDataObj=storedSymbolObj(testDataFilename)
testDataObj.makeTablePng(outputFilename)