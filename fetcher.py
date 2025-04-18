from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, select, and_

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")

metadata = MetaData(schema="public")

def fetch_data():
    today = datetime.today()
    before = today - timedelta(days=368)
    after = today - timedelta(days=358)
    schedule_tbl = Table("schedule", metadata, autoload_with=engine)
    with engine.connect() as conn:
        query = (
            select(schedule_tbl)
            .where(and_(
                schedule_tbl.c.SEASON_ID == 2024,
                schedule_tbl.c.G_DT > before.strftime("%Y%m%d"),
                schedule_tbl.c.G_DT < after.strftime("%Y%m%d"),
            ))
           .order_by(schedule_tbl.c.G_DT)
        )   
        result = conn.execute(query).fetchall()
        return result
