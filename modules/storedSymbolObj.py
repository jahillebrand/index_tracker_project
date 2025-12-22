# Import os, Json, and plotting utilities
import os
import json
import matplotlib.pyplot as plt

class storedSymbolObj:
    def __init__(self, jsonFilename):
        # Prep object data
        self.filename = jsonFilename
        self.symbolDataList = []
        self.sortedSymbolDataList = []
        self.importJsonDataFromFile(self.filename)

    # Function to pull in json data
    def importJsonDataFromFile(self,jsonFilename):
        # Read the stored Json file
        with open(jsonFilename, 'r') as file:
            tempJsonFiledata=json.load(file)

        # Copy symbol data objects into self.symbolDataList in expected format
        for line in tempJsonFiledata['symbolData']:
            self.symbolDataList.append(line)

        # Sort the list and copy it into self.sortedSymbolDataList, greatest return to least
        self.sortedSymbolDataList = sorted(
            self.symbolDataList,
            key=lambda d: d['tenYearTenKUsdReturn'],
            reverse=True
        )


    # ChatGPT gave me this to make a png
    def makeTablePng(self, outputPath=None):
        # If no argument is given, output to same filename as given in constructor
        baseJsonFilename, _ = os.path.splitext(self.filename)
        pngDefaultFilename = baseJsonFilename + ".png"
        if outputPath is None:
            outputPath = pngDefaultFilename

        # Build the table row-by-row, top to bottom
        # Easy, readable, and does exactly what we want
        tableData = []

        for rowDict in self.sortedSymbolDataList:
            # Symbols should always look sharp — uppercase cleans it up
            symbolValue = str(rowDict["symbol"]).upper()

            # Format the 10-year return like real money:
            # dollar sign, commas, and two clean decimals
            tenYearValue = rowDict["tenYearTenKUsdReturn"]
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