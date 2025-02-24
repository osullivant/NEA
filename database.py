import sqlite3


class Database:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(f"{dbName}.db")
        self.cur = self.conn.cursor()
        self.createUserTable()

    def createAllTables(self):
        self.createUserTable()
        self.createGameTable()
        self.createGameplayTable()

    def createUserTable(self):
        sql = """
        CREATE TABLE IF NOT EXISTS User(
            UserID INTEGER PRIMARY KEY,
            FName TEXT NOT NULL,
            LName TEXT NOT NULL,
            Email Varchar(320) NOT NULL,
            Password TEXT NOT NULL
            ) 
        """

        self.cur.execute(sql)
        self.conn.commit()

    def createGameTable(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Game(
            GameID INTEGER PRIMARY KEY,
            SimType INTEGER NOT NULL,
            PredPrey TEXT NOT NULL,
            StartPred INTEGER NOT NULL,
            StartPrey INTEGER NOT NULL,
            EndPred INTEGER NOT NULL,
            EndPrey INTEGER NOT NULL,
            Steps INTEGER NOT NULL
            ) 
        """

        self.cur.execute(sql)
        self.conn.commit()

    def createGameplayTable(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Gameplay(
            GameplayID INTEGER PRIMARY KEY,
            UserID INTEGER NOT NULL,
            GameID INTEGER NOT NULL,
            Date DATETIME NOT NULL,
            FOREIGN KEY(UserID) REFERENCES User(UserID)
            FOREIGN KEY(GameID) REFERENCES Game(GameID)
            )
        """

        self.cur.execute(sql)
        self.conn.commit()

    def deleteTable(self, tableName):
        sql = f"DROP TABLE {tableName}"
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print(f"Table {tableName} deleted")
        except:
            print(f"Table '{tableName}' not in database")


if __name__ == "__main__":
    db = Database("Evolution")
    option = 1
    while option in [1, 2]:
        option = int(input("1: Refresh all tables \n2: Delete a table\n"))
        if option == 1:
            db.createAllTables()
            print("Tables Created")
        elif option == 2:
            tableName = input("Name of table to be deleted: ")
            if input(f"Are you sure you want to delete {tableName} table? Y/N: ").upper() == "Y":
                db.deleteTable(tableName)
