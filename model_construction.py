"""Build and compile model."""
import sqlite3

con = sqlite3.connect("C:/Users/jacks/BIOSTAT821/Final_Project/NBA-Best/nba.db")
# con = sqlite3.connect("nba.db")

cur = con.cursor()

query1 = "SELECT * FROM PlayerStats"
test = cur.execute(query1)
# for i in test:
#     print(i)

query2 = """
        SELECT ps.Name, Position, GamesPlayed - GamesStarted
        FROM PlayerStats ps
        LEFT JOIN Salary s
        ON ps.Name = s.Name
        ORDER BY s.Salary2122 DESC
        """
test2 = cur.execute(query2)
for i in test2:
    print(i)
