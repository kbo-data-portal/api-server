from datetime import datetime, timedelta
from sqlalchemy import select, and_, func, desc, or_

from fetcher import ENGINE, TABLES


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
        )
        return conn.execute(query).fetchall()


def fetch_game_schedule_by_date(date: datetime = None, teams: list = None):
    table = TABLES["game_schedule"]
    with ENGINE.connect() as conn:
        conditions = []

        if date:
            conditions.append(table.c["G_DT"] == date.strftime("%Y%m%d"))
        else:
            conditions.append(table.c["G_DT"] >= datetime.now().strftime("%Y%m%d"))

        if teams:
            if len(teams) > 1:
                conditions.append(or_(
                    and_(table.c["HOME_NM"] == teams[0], table.c["AWAY_NM"] == teams[1]),
                    and_(table.c["HOME_NM"] == teams[1], table.c["AWAY_NM"] == teams[0])
                ))
            else:
                conditions.append(or_(
                    table.c["HOME_NM"] == teams[0], table.c["AWAY_NM"] == teams[0]
                ))

        query = (
            select(
                table.c["SEASON_ID"],
                table.c["G_ID"],
                table.c["G_DT"],
                table.c["G_DT_TXT"],
                table.c["G_TM"],
                table.c["S_NM"],
                table.c["HOME_ID"],
                table.c["HOME_NM"],
                table.c["AWAY_NM"],
            )
            .where(and_(*conditions))
            .order_by(table.c["G_DT"])
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
    table = TABLES["game_result"]
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

