import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import Engine, URL

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = 5432
DB_NAME = os.getenv("DB_NAME", "postgres")


def _get_engine() -> Engine:
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
    return create_engine(url)


ENGINE = _get_engine()

meta_game = MetaData(schema="game")
meta_player = MetaData(schema="player")
meta_analytics = MetaData(schema="analytics")

TABLES = {
    "game_schedule": Table("schedule", meta_game, autoload_with=ENGINE),
    "game_result": Table("result", meta_game, autoload_with=ENGINE),
    "game_prediction": Table("prediction", meta_game, autoload_with=ENGINE),
    "player_pitcher": Table(
        "pitcher_season_summary", meta_player, autoload_with=ENGINE
    ),
    "player_hitter": Table("hitter_season_summary", meta_player, autoload_with=ENGINE),
    "team_summary": Table(
        "fct_team_result_summary", meta_analytics, autoload_with=ENGINE
    ),
    "team_vs_summary": Table(
        "fct_team_vs_summary", meta_analytics, autoload_with=ENGINE
    ),
    "team_pitcher": Table(
        "fct_team_pitcher_stats", meta_analytics, autoload_with=ENGINE
    ),
    "team_hitter": Table("fct_team_hitter_stats", meta_analytics, autoload_with=ENGINE),
}
