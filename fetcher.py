from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, select, and_, func, over
from sqlalchemy.sql import desc

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
metadata = MetaData(schema="public")

def fetch_game_list():
    today = datetime.today()
    before = today - timedelta(days=3)
    after = today + timedelta(days=7)
    tbl = Table("game_schedule", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(
                tbl.c["G_ID"],
                tbl.c["G_DT_TXT"],
                tbl.c["G_TM"],
                tbl.c["S_NM"],
                tbl.c["AWAY_ID"],
                tbl.c["AWAY_NM"],
                tbl.c["HOME_ID"],
                tbl.c["HOME_NM"],
                func.coalesce(tbl.c["T_PIT_P_NM"], "미정").label("T_PIT_P_NM"),
                func.coalesce(tbl.c["B_PIT_P_NM"], "미정").label("B_PIT_P_NM"),
                tbl.c["T_PIT_P_NM"],
                tbl.c["B_PIT_P_NM"],
                tbl.c["SEASON_ID"]
            )
            .where(and_(
                tbl.c["G_DT"] > before.strftime("%Y%m%d"),
                tbl.c["G_DT"] < after.strftime("%Y%m%d"),
            ))
           .order_by(tbl.c["G_DT"])
        )   
        return conn.execute(query).fetchall()


def fetch_match_info(game_id):
    tbl = Table("game_schedule", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(
                tbl.c["SEASON_ID"],
                tbl.c["AWAY_ID"],
                tbl.c["AWAY_NM"],
                tbl.c["HOME_ID"],
                tbl.c["HOME_NM"],
                tbl.c["G_DT_TXT"],
                tbl.c["TV_IF"],
                tbl.c["S_NM"]
            )
            .where(tbl.c["G_ID"] == game_id)
        )   
        return conn.execute(query).fetchone()


def fetch_op_match_info(home, away):
    tbl = Table("game_summary", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(
                tbl.c["G_DT"],
                tbl.c["HOME_NM"], 
                tbl.c["AWAY_NM"],
                func.max(tbl.c["B_SCORE_CN"]).label("HOME_SCORE"),
                func.max(tbl.c["T_SCORE_CN"]).label("AWAY_SCORE")
            )
            .where(and_(
                tbl.c["HOME_NM"].in_([home, away]),
                tbl.c["AWAY_NM"].in_([home, away])
            ))
            .group_by(tbl.c["G_DT"], tbl.c["HOME_NM"], tbl.c["AWAY_NM"])
            .order_by(desc(tbl.c["G_DT"]))
            .limit(5)
        )   
        return conn.execute(query).fetchall()


def fetch_rank_info(season):
    tbl = Table("team_summary", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(
                tbl.c["TEAM_NM"],
                tbl.c["W_CN"],
                tbl.c["L_CN"],
                tbl.c["D_CN"],
                func.rank().over(order_by=desc(tbl.c["W_RATE"])).label("RANK")
            )
            .where(tbl.c["SEASON_ID"] == season)
        )   
        return conn.execute(query).fetchall()
    

def fetch_op_rank_info(season, home, away):
    tbl = Table("team_op_summary", metadata, autoload_with=engine)
    with engine.connect() as conn:
        if season > 0:
            query = (
                select(
                    tbl.c["W_CN"],
                    tbl.c["L_CN"],
                    tbl.c["D_CN"],
                    tbl.c["R"],
                    tbl.c["H"],
                    tbl.c["B"],
                    tbl.c["E"]
                )
                .where(and_(
                    tbl.c["SEASON_ID"] == season,
                    tbl.c["TEAM_NM"] == home,
                    tbl.c["OP_NM"] == away
                ))
            )   
        else:
            query = (
                select(
                    func.sum(tbl.c["W_CN"]).label("W_CN"),
                    func.sum(tbl.c["L_CN"]).label("L_CN"),
                    func.sum(tbl.c["D_CN"]).label("D_CN"),
                    func.sum(tbl.c["R"]).label("R"),
                    func.sum(tbl.c["H"]).label("H"),
                    func.sum(tbl.c["B"]).label("B"),
                    func.sum(tbl.c["E"]).label("E")
                )
                .where(and_(
                    tbl.c["TEAM_NM"] == home,
                    tbl.c["OP_NM"] == away
                ))
                .group_by(tbl.c["TEAM_NM"], tbl.c["OP_NM"])
            )   
        return conn.execute(query).fetchone()
    
    
def fetch_pitcher_info(season, team):
    tbl = Table("team_pitcher", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(
                func.sum(tbl.c["W_CN"]).label("W_CN"),
                func.sum(tbl.c["L_CN"]).label("L_CN"),
                func.sum(tbl.c["D_CN"]).label("D_CN"),
                func.sum(tbl.c["R"]).label("R"),
                func.sum(tbl.c["H"]).label("H"),
                func.sum(tbl.c["B"]).label("B"),
                func.sum(tbl.c["E"]).label("E")
            )
            .where(and_(
                tbl.c["SEASON_ID"] == season,
                tbl.c["TEAM_NM"] == team
            ))
            .group_by(tbl.c["TEAM_NM"], tbl.c["OP_NM"])
        )   
        return conn.execute(query).fetchone()
    

def fetch_hitter_info(season, team):
    tbl = Table("team_hitter", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(
                tbl.c["R"],
                tbl.c["H"],
                tbl.c["HR"],
                tbl.c["RBI"],
                tbl.c["2B"],
                tbl.c["3B"],
                tbl.c["BB"],
                tbl.c["SO"]
            )
            .where(and_(
                tbl.c["SEASON_ID"] == 2024,
                tbl.c["TEAM_NM"] == team
            ))
        )   
        return conn.execute(query).fetchone()