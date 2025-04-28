from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, select, and_, func, asc, desc, or_

ENGINE = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
TABLES = {
    "game_schedule": Table("game_schedule", MetaData(schema="public"), autoload_with=ENGINE),
    "game_summary": Table("game_summary", MetaData(schema="public"), autoload_with=ENGINE),      
    "player_pitcher_stats": Table("player_pitcher_stats", MetaData(schema="public"), autoload_with=ENGINE),
    "player_hitter_stats": Table("player_hitter_stats", MetaData(schema="public"), autoload_with=ENGINE),
    "team_summary": Table("fct_team_season_summary", MetaData(schema="analytics"), autoload_with=ENGINE),
    "team_vs_summary": Table("fct_team_vs_summary", MetaData(schema="analytics"), autoload_with=ENGINE),
    "team_pitcher": Table("fct_team_pitcher_stats", MetaData(schema="analytics"), autoload_with=ENGINE),
    "team_hitter": Table("fct_team_hitter_stats", MetaData(schema="analytics"), autoload_with=ENGINE),
}

def fetch_recent_games():
    today = datetime.today()
    start_date = today - timedelta(days=3)
    end_date = today + timedelta(days=7)

    table = TABLES["game_schedule"]
    with ENGINE.connect() as conn:
        query = (
            select(
                table.c["G_ID"],
                table.c["G_DT_TXT"],
                table.c["G_TM"],
                table.c["S_NM"],
                table.c["AWAY_ID"],
                table.c["AWAY_NM"],
                table.c["HOME_ID"],
                table.c["HOME_NM"],
                func.coalesce(table.c["T_PIT_P_NM"], "미정").label("T_PIT_P_NM"),
                func.coalesce(table.c["B_PIT_P_NM"], "미정").label("B_PIT_P_NM"),
                table.c["SEASON_ID"]
            )
            .where(and_(
                table.c["G_DT"] > start_date.strftime("%Y%m%d"),
                table.c["G_DT"] < end_date.strftime("%Y%m%d"),
            ))
            .order_by(table.c["G_DT"])
            .limit(40)
        )
        return conn.execute(query).fetchall()


def fetch_game_info_by_id(game_id: str):
    table = TABLES["game_schedule"]
    with ENGINE.connect() as conn:
        query = (
            select(
                table.c["SEASON_ID"],
                table.c["AWAY_ID"],
                table.c["AWAY_NM"],
                table.c["HOME_ID"],
                table.c["HOME_NM"],
                table.c["G_DT_TXT"],
                func.coalesce(table.c["TV_IF"], "미정").label("TV_IF"),
                table.c["S_NM"]
            )
            .where(table.c["G_ID"] == game_id)
        )
        return conn.execute(query).fetchone()


def fetch_head_to_head_recent_games(home_team: str, away_team: str):
    table = TABLES["game_summary"]
    with ENGINE.connect() as conn:
        query = (
            select(
                table.c["G_DT"],
                table.c["HOME_NM"],
                table.c["AWAY_NM"],
                func.max(table.c["B_SCORE_CN"]).label("HOME_SCORE"),
                func.max(table.c["T_SCORE_CN"]).label("AWAY_SCORE")
            )
            .where(or_(
                and_(table.c["HOME_NM"] == home_team, table.c["AWAY_NM"] == away_team, table.c["SR_ID"] == 0),
                and_(table.c["HOME_NM"] == away_team, table.c["AWAY_NM"] == home_team, table.c["SR_ID"] == 0)
            ))
            .group_by(table.c["G_DT"], table.c["HOME_NM"], table.c["AWAY_NM"])
            .order_by(desc(table.c["G_DT"]))
            .limit(5)
        )
        return conn.execute(query).fetchall()


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
                    table.c["OP_NM"] == opponent_name
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
                    table.c["OP_NM"] == opponent_name
                ))
                .group_by(table.c["TEAM_NM"], table.c["OP_NM"])
            )
        return conn.execute(query).fetchone()


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
        return conn.execute(query).fetchone()


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
        return conn.execute(query).fetchone()


def fetch_player_pitching_stats(season_id: int, team_name: str = None):
    table = TABLES["player_pitcher_stats"]
    with ENGINE.connect() as conn:
        if team_name:
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
                .where(and_(
                    table.c["SEASON_ID"] == season_id,
                    table.c["TEAM_NM"] == team_name,
                    table.c["IP"] > table.c["G"] * 1.6
                ))
                .limit(10)
            )
        else:
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
                .where(and_(
                    table.c["SEASON_ID"] == season_id,
                    table.c["IP"] > table.c["G"] * 1.6
                ))
                .limit(10)
            )
        return conn.execute(query).fetchall()


def fetch_player_hitting_stats(season_id: int, team_name: str = None):
    table = TABLES["player_hitter_stats"]
    with ENGINE.connect() as conn:
        if team_name:
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
                .where(and_(
                    table.c["SEASON_ID"] == season_id,
                    table.c["TEAM_NM"] == team_name,
                    table.c["PA"] > table.c["G"] * 3.1
                ))
                .limit(10)
            )
        else:
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
                .where(and_(
                    table.c["SEASON_ID"] == season_id,
                    table.c["PA"] > table.c["G"] * 3.1
                ))
                .limit(10)
            )
        return conn.execute(query).fetchall()
