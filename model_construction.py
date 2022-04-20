"""Build and compile model."""
import sqlite3

con = sqlite3.connect("C:/Users/jacks/BIOSTAT821/Final_Project/NBA-Best/nba.db")

cur = con.cursor()


def get_max(column: str, position: str):
    "Get max value for a given variable."
    max = cur.execute(
        f"""
        SELECT MAX({column}) FROM PlayerStats
        WHERE GamesPlayed > 15
        AND ThreePointersAttempted > 2
        AND Position IN ({position})
        """,
        # The ThreePointersAttempted variable is actually the average number of
        # 3 pointers attempted per game, so I decied that 2 was a reasonable
        # average to reduce an individual playing in just a few games and
        # hitting most of his 3's
    )
    return max.fetchone()[0]


# print(get_max("ThreePointersPct"))
# print(get_max("Assists"))
# print(get_max("Turnovers"))
print("start")
test_pos = "'PG', 'SG'"
print(get_max("Assists / Turnovers", test_pos))
print("break")
# My idea is to normalize each of the metrics by the maximum value in all of
# the data, since this is a competition then we can compare individuals to
# others

# The argument could be made that since we are selecting players by position,
# then we should normalize by the max for a specific metric only among players
# in that same position, which is very fair. BUT I am going to start more
# simple than that.

# UPDATE: I added in the funcitonality to only include players in that position
# for the maximum calculation.

ass_turn = cur.execute(
    """SELECT Name FROM PlayerStats WHERE (Assists / Turnovers) > 7 AND
    GamesPlayed > 15 AND ThreePointersAttempted > 2"""
)
print(ass_turn.fetchall())

tyus_jones = cur.execute(
    """SELECT 
        GamesPlayed,
        Assists,
        Turnovers
    FROM PlayerStats WHERE Name = 'Tyus Jones'
    """
)
print(tyus_jones.fetchone())


def normalize_query(position: str):
    query = f"""
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersPct / {get_max("ThreePointersPct", position)},3),
                ROUND((Assists / Turnovers) / {get_max("Assists / Turnovers", position)},3),
                ROUND(Steals / {get_max("Steals", position)}, 3),
                ROUND(OffensiveRebounds / {get_max("OffensiveRebounds", position)}, 3),
                ROUND((FreeThrowsAttempted * FreeThrowPct) / 
                    {get_max("FreeThrowsAttempted * FreeThrowPct", position)},3),
                TwoPointersAttempted,
                TwoPointersMade
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ({position})
            ORDER BY s.Salary2122
            """
    return query


guards = cur.execute(normalize_query("'PG', 'SG'"))
for i in guards:
    print(i)
