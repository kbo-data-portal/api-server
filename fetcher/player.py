from sqlalchemy import select, and_, func, asc, desc

from fetcher import ENGINE, TABLES


def fetch_player_pitching_stats(season_id: int, team_name: str = None):
    table = TABLES["player_pitcher"]
    with ENGINE.connect() as conn:
        game_avg = conn.execute(select(func.avg(table.c["G"]))).fetchone()[0]
        conditions = [
            table.c["SEASON_ID"] == season_id,
            table.c["G"] > float(game_avg) / 1.5
        ]

        if team_name:
            conditions.append([
                table.c["TEAM_NM"] == team_name,
                table.c["IP"] > table.c["G"] * 2.65
            ])
        else:
            conditions.append([
                table.c["TEAM_NM"] == team_name,
                table.c["IP"] > table.c["G"] * 5.3
            ])
            
        query = (
            select(
                table.c["P_ID"],
                table.c["P_NM"],
                table.c["TEAM_NM"],
                table.c["ERA"],
                table.c["W"],
                table.c["SO"],
                func.rank().over(order_by=asc(table.c["ERA"])).label("RANK")
            )
            .where(and_(*conditions))
            .limit(10)
        )
        return conn.execute(query).fetchall()


def fetch_player_hitting_stats(season_id: int, team_name: str = None):
    table = TABLES["player_hitter"]
    with ENGINE.connect() as conn:
        game_avg = conn.execute(select(func.avg(table.c["G"]))).fetchone()[0]
        conditions = [
            table.c["SEASON_ID"] == season_id,
            table.c["G"] > float(game_avg) / 1.5
        ]

        if team_name:
            conditions.append([
                table.c["TEAM_NM"] == team_name,
                table.c["PA"] > table.c["G"] * 1.8
            ])
        else:
            conditions.append([
                table.c["TEAM_NM"] == team_name,
                table.c["PA"] > table.c["G"] * 3.6
            ])

        query = (
            select(
                table.c["P_ID"],
                table.c["P_NM"],
                table.c["TEAM_NM"],
                table.c["AVG"],
                table.c["R"],
                table.c["H"],
                table.c["HR"],
                func.rank().over(order_by=desc(table.c["AVG"])).label("RANK")
            )
            .where(and_(*conditions))
            .limit(10)
        )
        return conn.execute(query).fetchall()

