# Import os, Json, and plotting utilities
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

class storedSymbolObj:
    # Constants
    exactDaysPerYear=365.2425

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
        for symbol in tempJsonFiledata:
            self.symbolDataList.append(tempJsonFiledata[symbol])

        # Sort the list and copy it into self.sortedSymbolDataList, greatest return to least
        self.sortedSymbolDataList = sorted(
            self.symbolDataList,
            key=lambda d: float(d['tenYearCagr']),
            reverse=True
        )


    # ChatGPT gave me this to make a png
    def makeTablePng(self, outputPath=None):
        # If no argument is given, output to same filename as given in constructor
        fileArray = self.filename.replace("/",".").split(".")
        tableExportFilename = f"exports/{fileArray[1]}.pdf"
        if outputPath is None:
            outputPath = tableExportFilename

        # Build the table row-by-row, top to bottom
        # Easy, readable, and does exactly what we want
        tableData = []

        for rowDict in self.sortedSymbolDataList:
            # Symbols should always look sharp — uppercase cleans it up
            symbolValue = str(rowDict["symbol"]).upper()

            # Symbol Name - strip off a bunch of stuff we don't need to show
            fundName = str(
                rowDict["fundName"]).replace(
                    "VANGUARD","").replace(
                        "INVESTOR SHARES","").replace(
                            "ADMIRAL SHARES","")

            # Format the 10-year return like real money:
            # dollar sign, commas, and two clean decimals
            tenYearValue = rowDict["tenYearTenKUsdReturn"]
            formattedReturn = f"${float(tenYearValue):,.2f}"

            # Format the 10 year Cagr as a percent to 2 decimal places
            tenYearCagr = rowDict["tenYearCagr"]
            formattedCagr = f"{float(tenYearCagr):,.2f}%"

            # Calculate the number of years used for Cagr
            dateLastUpdatedStr = rowDict["dateLastUpdated"]
            tenYearDateStr = rowDict["tenYearDate"]
            dateLastUpdated = datetime.strptime(
                dateLastUpdatedStr,
                "%Y-%m-%d"
                ).date()
            tenYearDate = datetime.strptime(
                tenYearDateStr,
                "%Y-%m-%d"
                ).date()
            calculatedYears = float((dateLastUpdated - tenYearDate).days / 
                                    storedSymbolObj.exactDaysPerYear)
            formattedYears = f"{calculatedYears:,.2f}"

            tableData.append([
                symbolValue, 
                fundName,
                formattedReturn,
                formattedCagr,
                formattedYears,
                tenYearDateStr,
                dateLastUpdatedStr,
                ])

        # Column headers — short, clear, and professional
        columnLabels = [
            "Symbol",
            "Fund Name", 
            "10-year, $10k Return",
            "Annualized CAGR <10 yr",
            "Time Period",
            "First Date",
            "Last Date"
            ]
        # Figure size scales with number of rows so nothing feels cramped
        fig, ax = plt.subplots(figsize=(11, len(tableData) * 0.35))
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
        # Custom column widths to accommodate data
        baseWidth = table.get_celld()[(0,0)].get_width()

        for (rowIndex, colIndex), cell in table.get_celld().items():
            if rowIndex == 0:
                cell.set_text_props(weight="bold")
            #if colIndex == 1 and rowIndex != 0:
            #    cell.set_text_props(ha="right")
            if colIndex == 1:
                cell.set_width(baseWidth * 3.3)
                cell.set_text_props(ha="left")
            elif rowIndex != 0:
                cell.set_text_props(ha="center")
            if colIndex == 2:
                cell.set_width(baseWidth * 1.5)
            if colIndex == 3:
                cell.set_width(baseWidth * 1.8)

        # Save it out crisp and print-ready
        plt.savefig(outputPath, bbox_inches="tight", dpi=200)
        plt.close(fig)