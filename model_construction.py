"""Build and compile model."""
import sqlite3

con = sqlite3.connect("nba.db")

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
# print("start")
# test_pos = "'PG', 'SG'"
# print(get_max("TwoPointersAttempted", test_pos))
# print(get_max("TwoPointersPct", test_pos))

# attempt2 = cur.execute("SELECT Name FROM PlayerStats WHERE TwoPointersAttempted = 16.2")
# print(attempt2.fetchone())

# the highest 2ptPct is .673, Matisse Thybulle, but his avg 2pAttempt is only
# 2.4.... should I include him?
# I think it is actually ok because we are also multiplying by the number of 2
# pointers made, so his score wont actually be the highest (likely)

# pct2 = cur.execute(
#     "SELECT Name, TwoPointersAttempted FROM PlayerStats WHERE TwoPointersPct = .673"
# )
# print(pct2.fetchone())

# My idea is to normalize each of the metrics by the maximum value in all of
# the data, since this is a competition then we can compare individuals to
# others

# The argument could be made that since we are selecting players by position,
# then we should normalize by the max for a specific metric only among players
# in that same position, which is very fair. BUT I am going to start more
# simple than that.

# UPDATE: I added in the funcitonality to only include players in that position
# for the maximum calculation.

# ass_turn = cur.execute(
#     """SELECT Name FROM PlayerStats WHERE (Assists / Turnovers) > 7 AND
#     GamesPlayed > 15 AND ThreePointersAttempted > 2"""
# )
# print(ass_turn.fetchall())

# tyus_jones = cur.execute(
#     """SELECT
#         GamesPlayed,
#         Assists,
#         Turnovers
#     FROM PlayerStats WHERE Name = 'Tyus Jones'
#     """
# )
# print(tyus_jones.fetchone())

###############################################################################
# Guards
###############################################################################


def guard_normalize_query(position: str):
    """Create columns that are normalized."""
    query = f"""
        CREATE TABLE GuardsNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersAttempted  * ThreePointersPct /
                    {get_max("ThreePointersAttempted * ThreePointersPct",
                    position)},3) AS j_threes,
                ROUND((Assists / Turnovers) / {get_max("Assists / Turnovers",
                    position)},3) AS j_atr,
                ROUND(Steals / {get_max("Steals", position)}, 3) AS j_stl,
                ROUND(OffensiveRebounds / {get_max("OffensiveRebounds",
                    position)}, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    {get_max("FreeThrowsAttempted * FreeThrowPct",
                    position)},3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    {get_max("TwoPointersAttempted * TwoPointersPct",
                    position)},3) AS j_twos
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ({position})
            ORDER BY s.Salary2122
            """
    return query


cur.execute("DROP TABLE IF EXISTS GuardsNormalizedStats")
# print(guard_normalize_query("'PG', 'SG'"))
cur.execute(guard_normalize_query("'PG', 'SG'"))
con.commit()

# This was useful before I created the table as the select statement
# guards = cur.execute(normalize_query("'PG', 'SG'"))
# for i in guards:
#     print(i)
# guards = cur.execute("SELECT * FROM GuardsNormalizedStats")
# for i in guards:
#     print(i)


def guard_selections(table: str, number_players: int):
    "Make Selections."
    query = f"""
    SELECT 
        Name,
        (j_threes + j_atr + j_stl + j_or + j_ft + j_twos) * (100 / 6) AS rank
    FROM {table}
    ORDER BY rank DESC
    LIMIT {number_players}
    """
    return query


top5 = []
guard_ranked = cur.execute(guard_selections("GuardsNormalizedStats", 2))
for i in guard_ranked:
    top5.append(i[0])
    print(i)


###############################################################################
# Forwards
###############################################################################


def forward_normalize_query(position: str):
    "Create columns that are normalized"
    query = f"""
        CREATE TABLE ForwardsNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersAttempted  * ThreePointersPct /
                    {get_max("ThreePointersAttempted * ThreePointersPct",
                    position)},3) AS j_threes,
                ROUND((Assists / Turnovers) / {get_max("Assists / Turnovers",
                    position)},3) AS j_atr,
                ROUND(DefensiveRebounds / {get_max("DefensiveRebounds",
                    position)}, 3) AS j_dr,
                ROUND(OffensiveRebounds / {get_max("OffensiveRebounds",
                    position)}, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    {get_max("FreeThrowsAttempted * FreeThrowPct",
                    position)},3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    {get_max("TwoPointersAttempted * TwoPointersPct",
                    position)},3) AS j_twos,
                ROUND(Blocks / {get_max("Blocks", position)}, 3) AS j_blocks
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ({position})
            ORDER BY s.Salary2122
            """
    return query


cur.execute("DROP TABLE IF EXISTS ForwardsNormalizedStats")
cur.execute(forward_normalize_query("'PF', 'SF'"))
con.commit()


def forward_selections(table: str, number_players: int):
    "Make Selections."
    query = f"""
    SELECT 
        Name,
        (j_threes + j_atr + j_dr + j_or + j_ft + j_twos + j_blocks) * (100 / 7) AS rank
    FROM {table}
    ORDER BY rank DESC
    LIMIT {number_players}
    """
    return query


forward_ranked = cur.execute(forward_selections("ForwardsNormalizedStats", 2))
for i in forward_ranked:
    top5.append(i[0])
    print(i)

# testing = cur.execute(
#     "SELECT COUNT(Name) FROM PlayerStats WHERE Position IN ('PF', 'SF')"
# )
# for i in testing:
#     print(i)


###############################################################################
# Centers
###############################################################################


def center_normalize_query(position: str):
    "Create columns that are normalized"
    query = f"""
        CREATE TABLE CentersNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND((Assists / Turnovers) / {get_max("Assists / Turnovers",
                    position)},3) AS j_atr,
                ROUND(DefensiveRebounds / {get_max("DefensiveRebounds",
                    position)}, 3) AS j_dr,
                ROUND(OffensiveRebounds / {get_max("OffensiveRebounds",
                    position)}, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    {get_max("FreeThrowsAttempted * FreeThrowPct",
                    position)},3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    {get_max("TwoPointersAttempted * TwoPointersPct",
                    position)},3) AS j_twos,
                ROUND(Blocks / {get_max("Blocks", position)}, 3) AS j_blocks
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ({position})
            ORDER BY s.Salary2122
            """
    return query


cur.execute("DROP TABLE IF EXISTS CentersNormalizedStats")
cur.execute(center_normalize_query("'C'"))
con.commit()


def center_selections(table: str, number_players: int):
    "Make Selections."
    query = f"""
    SELECT 
        Name,
        (j_atr + j_dr + j_or + j_ft + j_twos + j_blocks) * (100 / 6) AS rank
    FROM {table}
    ORDER BY rank DESC
    LIMIT {number_players}
    """
    return query


center_ranked = cur.execute(center_selections("CentersNormalizedStats", 3))
for i in center_ranked:
    top5.append(i[0])
    print(i)

salaryTop5 = []
for i in top5:
    salary = cur.execute(f"SELECT Salary2122 FROM Salary WHERE Name = '{i}'")
    for j in salary:
        salaryTop5.append(j[0])

# print(salaryTop5)
# print(sum(salaryTop5))


# testing = cur.execute("SELECT COUNT(Name) FROM PlayerStats WHERE Position IN ('C')")
# for i in testing:
#     print(i)
