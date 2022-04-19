"""Build and compile model."""
import sqlite3

con = sqlite3.connect("C:/Users/jacks/BIOSTAT821/Final_Project/NBA-Best/nba.db")

cur = con.cursor()

# query1 = "SELECT * FROM PlayerStats"
# test = cur.execute(query1)
# for i in test:
#     print(i)

# DECLARE @var1 VARCHAR(255);

# SELECT @var1 = MAX(ThreePointersPct)
# FROM PlayerStats


def get_max(column: str):
    "Get max value for a given variable."
    # column_iterable = [column]
    max = cur.execute(
        f"""
        SELECT MAX({column}) FROM PlayerStats
        WHERE ThreePointersAttempted > 2
        """,
        # The ThreePointersAttempted variable is actually the average number of
        # 3 pointers attempted per game, so I decied that 2 was a reasonable
        # average to reduce an individual playing in just a few games and
        # hitting most of his 3's
    )
    return max.fetchone()[0]


print(get_max("ThreePointersPct"))

# test = cur.execute(
#     """SELECT MAX(ThreePointersPct) FROM PlayerStats WHERE ThreePointersAttempted > 2"""
# )
# print(test.fetchone())


query2 = f"""
        SELECT ps.Name, Position, ThreePointersPct * 100, ThreePointersPct / {get_max("ThreePointersPct")}
        FROM PlayerStats ps
        LEFT JOIN Salary s
        ON ps.Name = s.Name
        ORDER BY s.Salary2122 DESC
        """
test2 = cur.execute(query2)
for i in test2:
    print(i)
