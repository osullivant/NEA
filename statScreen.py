import tkinter as tk
from tkinterUtils import Field
import sqlite3
from database import Database


def parseStats(stats: list):
    FR1List = []
    WD1List = []
    FR2List = []
    WD2List = []
    for record in stats:
        if record[0] == 1:
            if record[1] == "Fox+Rabbit":
                FR1List.append(record)
            else:
                WD1List.append(record)
        else:
            if record[1] == "Fox+Rabbit":
                FR2List.append(record)
            else:
                WD2List.append(record)
    return [FR1List, WD1List, FR2List, WD2List]


class StatScreen:
    def __init__(self, userID):
        self.root = tk.Tk()
        self.root.geometry("600x500")
        self.root.config(bg="#3f0073")
        self.root.title("Stats")
        self.userID = userID
        self.statType = -1
        self.currentStat = 0
        self.parsedStats = ""

        self.textPanel = Field(75, 125, 450, 150, "Click on the buttons to view Local or Global Stats")
        self.textPanel.createLabel(self.root)

        titleText = Field(50, 25, 500, 50, "Local/Global Statistics")
        titleText.createLabel(self.root)

        localStatsButton = tk.Button(self.root, width=200, text="Local Statistics", command=self.localStats)
        localStatsButton.place(x=75, y=325, width=200, height=50)

        globalStatsButton = tk.Button(self.root, width=200, text="Global Statistics", command=self.globalStats)
        globalStatsButton.place(x=325, y=325, width=200, height=50)

        cycleStatsButton = tk.Button(self.root, width=200, text="Cycle Stats", command=self.cycleStats)
        cycleStatsButton.place(x=200, y=400, width=200, height=50)
        self.root.mainloop()

    def cycleStats(self):
        self.currentStat = (self.currentStat + 1) % 4
        usedStats = self.parsedStats[self.currentStat]
        print(usedStats)
        self.createStats(usedStats)

    def createStats(self, stats):
        simAnimalDict = {
            0: "Type 1 Sim, Foxes + Rabbits",
            1: "Type 1 Sim, Wolves + Deer",
            2: "Type 2 Sim, Foxes + Rabbits",
            3: "Type 2 Sim, Wolves + Deer"
        }
        if stats:
            endPred = []
            endPrey = []
            for stat in stats:
                endPred.append(stat[4])
                endPrey.append(stat[5])
            totalEndPred = sum(endPred)
            totalEndPrey = sum(endPrey)
            ratio = round(totalEndPrey / totalEndPred)
            descriptionText = f"Average predator : prey ratio 1 : {ratio}"
        else:
            descriptionText = "No data found for this simulation type"
        self.textPanel.label.config(text=f"{self.statType}:\n{simAnimalDict[self.currentStat]}:\n{descriptionText}")

    def localStats(self):
        self.statType = "Local"
        self.parsedStats = parseStats(self.getLocalStats())
        self.stats()

    def globalStats(self):
        self.statType = "Global"
        self.parsedStats = parseStats(self.getGlobalStats())
        self.stats()

    def stats(self):
        # self.currentStat = 0
        self.createStats(self.parsedStats[self.currentStat])

    def getLocalStats(self):
        db = Database("Evolution")
        sql = (f"SELECT SimType, PredPrey, StartPred, StartPrey, EndPred, Endprey, Steps FROM Game, Gameplay WHERE "
               f"Game.GameID = Gameplay.GameID and UserID = ?")
        records = db.cur.execute(sql, (self.userID,)).fetchall()
        db.conn.commit()
        return records

    def getGlobalStats(self):
        db = Database("Evolution")
        sql = (f"SELECT SimType, PredPrey, StartPred, StartPrey, EndPred, Endprey, Steps FROM Game, Gameplay WHERE "
               f"Game.GameID = Gameplay.GameID")
        records = db.cur.execute(sql, ()).fetchall()
        db.conn.commit()
        return records


if __name__ == "__main__":
    StatScreen(int(input("Enter userID: ")))
