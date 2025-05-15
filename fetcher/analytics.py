from sqlalchemy import select, and_, func, desc

from fetcher import ENGINE, TABLES


def fetch_team_rankings(season_id: int):
    table = TABLES["team_summary"]
    with ENGINE.connect() as conn:
        query = (
            select(
                table.c["TEAM_NM"],
                table.c["W_CN"],
                table.c["L_CN"],
                table.c["D_CN"],
                table.c["W_RATE"],
                func.rank().over(order_by=desc(table.c["W_RATE"])).label("RANK")
            )
            .where(table.c["SEASON_ID"] == season_id)
        )
        return conn.execute(query).fetchall()


def fetch_vs_team_stats(season_id: int, team_name: str, opponent_name: str):
    table = TABLES["team_vs_summary"]
    with ENGINE.connect() as conn:
        if season_id > 0:
            query = (
                select(
                    table.c["W_CN"],
                    table.c["L_CN"],
                    table.c["D_CN"],
                    table.c["R"],
                    table.c["H"],
                    table.c["B"],
                    table.c["E"]
                )
                .where(and_(
                    table.c["SEASON_ID"] == season_id,
                    table.c["TEAM_NM"] == team_name,
                    table.c["OPP_NM"] == opponent_name
                ))
            )
        else:
            query = (
                select(
                    func.sum(table.c["W_CN"]).label("W_CN"),
                    func.sum(table.c["L_CN"]).label("L_CN"),
                    func.sum(table.c["D_CN"]).label("D_CN"),
                    func.sum(table.c["R"]).label("R"),
                    func.sum(table.c["H"]).label("H"),
                    func.sum(table.c["B"]).label("B"),
                    func.sum(table.c["E"]).label("E")
                )
                .where(and_(
                    table.c["TEAM_NM"] == team_name,
                    table.c["OPP_NM"] == opponent_name
                ))
                .group_by(table.c["TEAM_NM"], table.c["OPP_NM"])
            )

        result = conn.execute(query).fetchone()
        if result is None:
            return { "W_CN": 0, "L_CN": 0, "D_CN": 0, "R": 0, "H": 0, "B": 0, "E": 0 }
        return result


def fetch_team_pitching_stats(season_id: int, team_name: str):
    table = TABLES["team_pitcher"]
    with ENGINE.connect() as conn:
        query = (
            select(
                table.c["W"],
                table.c["L"],
                table.c["SO"],
                table.c["BB"],
                table.c["SV"],
                table.c["HLD"],
                table.c["H"],
                table.c["ER"]
            )
            .where(and_(
                table.c["SEASON_ID"] == season_id,
                table.c["TEAM_NM"] == team_name
            ))
        )

        result = conn.execute(query).fetchone()
        if result is None:
            return { "W": 0, "L": 0, "SO": 0, "BB": 0, "SV": 0, "HLD": 0, "H": 0, "ER": 0 }
        return result


def fetch_team_hitting_stats(season_id: int, team_name: str):
    table = TABLES["team_hitter"]
    with ENGINE.connect() as conn:
        query = (
            select(
                table.c["R"],
                table.c["H"],
                table.c["HR"],
                table.c["RBI"],
                table.c["2B"],
                table.c["3B"],
                table.c["BB"],
                table.c["SO"]
            )
            .where(and_(
                table.c["SEASON_ID"] == season_id,
                table.c["TEAM_NM"] == team_name
            ))
        )
        
        result = conn.execute(query).fetchone()
        if result is None:
            return { "R": 0, "H": 0, "HR": 0, "RBI": 0, "2B": 0, "3B": 0, "BB": 0, "SO": 0 }
        return result

