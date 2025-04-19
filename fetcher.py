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
                tbl.c.G_ID,
                tbl.c.G_DT_TXT,
                tbl.c.G_TM,
                tbl.c.S_NM,
                tbl.c.AWAY_ID,
                tbl.c.AWAY_NM,
                tbl.c.HOME_ID,
                tbl.c.HOME_NM,
                func.coalesce(tbl.c.T_PIT_P_NM, "미정").label("T_PIT_P_NM"),
                func.coalesce(tbl.c.B_PIT_P_NM, "미정").label("B_PIT_P_NM"),
                tbl.c.T_PIT_P_NM,
                tbl.c.B_PIT_P_NM,
                tbl.c.SEASON_ID
            )
            .where(and_(
                tbl.c.G_DT > before.strftime("%Y%m%d"),
                tbl.c.G_DT < after.strftime("%Y%m%d"),
            ))
           .order_by(tbl.c.G_DT)
        )   
        return conn.execute(query).fetchall()


def fetch_match_info(game_id):
    tbl = Table("game_schedule", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(
                tbl.c.SEASON_ID,
                tbl.c.AWAY_ID,
                tbl.c.AWAY_NM,
                tbl.c.HOME_ID,
                tbl.c.HOME_NM,
                tbl.c.G_DT_TXT,
                tbl.c.TV_IF,
                tbl.c.S_NM
            )
            .where(tbl.c.G_ID == game_id)
        )   
        return conn.execute(query).fetchone()


def fetch_rank_info(season):
    tbl = Table("team_summary", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(
                tbl.c.TEAM_NM,
                tbl.c.W_CN,
                tbl.c.L_CN,
                tbl.c.D_CN,
                func.rank().over(order_by=desc(tbl.c.W_RATE)).label("RANK")
            )
            .where(and_(
                tbl.c.SEASON_ID == season
            ))
        )   
        return conn.execute(query).fetchall()