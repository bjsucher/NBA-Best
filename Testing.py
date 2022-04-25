"""Test functions for NBA-Best."""
from model_construction import (
    get_max,
    guard_normalize_query,
    forward_normalize_query,
    center_normalize_query,
)


def test_get_max():
    "Test the get_max function."
    assert get_max("TwoPointersPct", "'PG', 'SG'") == 0.673
    assert get_max("TwoPointersAttempted", "'PG', 'SG'") == 16.2
    assert round(get_max("Assists / Turnovers", "'PG', 'SG'"), 1) == 7.3
    assert get_max("Blocks", "'C'") == 2.8


def test_guard_normalize_query():
    "Test the guard_normalize_query function."
    assert (
        guard_normalize_query("'PG', 'SG'")
        == """
        CREATE TABLE GuardsNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersAttempted  * ThreePointersPct /
                    4.446,3) AS j_threes,
                ROUND((Assists / Turnovers) / 7.333333333333334,3) AS j_atr,
                ROUND(Steals / 2, 3) AS j_stl,
                ROUND(OffensiveRebounds / 1.8, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    6.5992,3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    8.6508,3) AS j_twos,
                ROUND(("Points") / 28.4) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ('PG', 'SG')
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    )


def test_forward_normalize_query():
    "Test the guard_normalize_query function."
    assert (
        forward_normalize_query("'PF', 'SF'")
        == """
        CREATE TABLE ForwardsNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND(ThreePointersAttempted  * ThreePointersPct /
                    3.0357999999999996,3) AS j_threes,
                ROUND((Assists / Turnovers) / 4.2,3) AS j_atr,
                ROUND(DefensiveRebounds / 9.6, 3) AS j_dr,
                ROUND(OffensiveRebounds / 2.6, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    8.2308,3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    9.24,3) AS j_twos,
                ROUND(Blocks / 2.3, 3) AS j_blocks,
                ROUND(Points / 30.3, 3) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ('PF', 'SF')
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    )


def test_center_normalize_query():
    "Test the center_normalzie_query function."
    assert (
        center_normalize_query("'C'")
        == """
        CREATE TABLE CentersNormalizedStats AS
            SELECT
                ps.Name,
                Position,
                ROUND((Assists / Turnovers) / 3.7777777777777777,3) AS j_atr,
                ROUND(DefensiveRebounds / 11, 3) AS j_dr,
                ROUND(OffensiveRebounds / 3.1, 3) AS j_or,
                ROUND((FreeThrowsAttempted * FreeThrowPct) /
                    9.6052,3) AS j_ft,
                ROUND((TwoPointersAttempted * TwoPointersPct) /
                    8.9976,3) AS j_twos,
                ROUND(Blocks / 2.8, 3) AS j_blocks,
                ROUND(Points / 30.6, 3) AS j_points
            FROM PlayerStats ps
            LEFT JOIN Salary s
            ON ps.Name = s.Name
            WHERE ps.Position IN ('C')
            AND GamesPlayed > 15
            AND ThreePointersAttempted > 2
            ORDER BY s.Salary2122
            """
    )
