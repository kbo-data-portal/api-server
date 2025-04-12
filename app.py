from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime, timedelta

APP = Flask(__name__)

def get_games():
    df = pd.read_csv('2025.csv')
    df['G_DT'] = pd.to_datetime(df['G_DT'], format='%Y%m%d')

    today = datetime.today()
    before = today - timedelta(days=3)
    after = today + timedelta(days=7)
    filtered_df = df[(df['G_DT'] >= before) & (df['G_DT'] <= after)]

    games = []

    for i in filtered_df.itertuples(index=False):
        games.append(
        {
            "game_sc": i.GAME_SC_ID, 
            "le_id": i.LE_ID, 
            "sr_id": i.SR_ID, 
            "season": i.SEASON_ID, 
            "g_id": i.G_ID, 
            "g_dt": i.G_DT,
            "s_nm": i.S_NM, 
            "vs_game_cn": i.VS_GAME_CN,
            "away_id": i.AWAY_ID, 
            "home_id": i.HOME_ID, 
            "away_nm": i.AWAY_NM, 
            "home_nm": i.HOME_NM, 
            "away_p_id": i.T_PIT_P_ID, 
            "home_p_id": i.B_PIT_P_ID, 
            "entry_ck": i.IE_ENTRY_CK,
            "start_ck": i.START_PIT_CK,
            "result_ck": i.GAME_RESULT_CK,
            "lineup_ck": i.LINEUP_CK,   
            "vod_ck": i.VOD_CK,
            "kbot_se": i.KBOT_SE,
            "gamedate_str": i.G_DT_TXT, 
            "time": i.G_TM,
            "away_pitcher": i.T_PIT_P_NM, 
            "home_pitcher": i.B_PIT_P_NM
        })

    return games

@APP.route("/")
def index():
    return render_template("index.html", games=get_games())

if __name__ == "__main__":
    APP.run(host="0.0.0.0")
