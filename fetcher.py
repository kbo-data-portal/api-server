from sqlalchemy import create_engine, MetaData, Table, select

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")

metadata = MetaData(schema="public")
player_table = Table("schedule", metadata, autoload_with=engine)

def fetch_data():
    with engine.connect() as conn:
        query = select(player_table).where(player_table.c.SEASON_ID == 2001).order_by(player_table.c.G_DT)
        result = conn.execute(query).fetchall()
        return result
