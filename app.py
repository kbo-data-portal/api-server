from flask import Flask, render_template, request, jsonify
from fetcher import fetch_game_list, fetch_match_info, fetch_rank_info, fetch_op_rank_info, fetch_op_match_info, fetch_hitter_info
from datetime import datetime

APP = Flask(__name__)

team = {
    "WO": {"full": "키움 히어로즈", "color": "#570514"},
    "OB": {"full": "두산 베어스", "color": "#1A1748"},
    "LT": {"full": "롯데 자이언츠", "color": "#041E42"},
    "SS": {"full": "삼성 라이온즈", "color": "#074CA1"},
    "HH": {"full": "한화 이글스", "color": "#FC4E00"},
    "HT": {"full": "KIA 타이거즈", "color": "#EA0029"},
    "LG": {"full": "LG 트윈스", "color": "#C30452"},
    "SK": {"full": "SSG 랜더스", "color": "#CE0E2D"},
    "NC": {"full": "NC 다이노스", "color": "#315288"},
    "KT": {"full": "KT 위즈", "color": "#000000"},
}

@APP.route("/get_match", methods=["POST"])
def get_match():
    data = request.get_json()
    game_id = data.get("game_id")

    match = fetch_match_info(game_id)
    rank = fetch_rank_info(match.SEASON_ID)
    op_rank = fetch_op_rank_info(0, match.HOME_NM, match.AWAY_NM)
    ss_op_rank = fetch_op_rank_info(match.SEASON_ID, match.HOME_NM, match.AWAY_NM)
    op_match = fetch_op_match_info(match.HOME_NM, match.AWAY_NM)
    
    home_hitter = fetch_hitter_info(match.SEASON_ID, match.HOME_NM)
    away_hitter = fetch_hitter_info(match.SEASON_ID, match.AWAY_NM)

    matches = []
    for row in op_match:
        matches.append({
            "G_DT": datetime.strptime(row.G_DT, "%Y-%m-%d").strftime("%Y년 %m월 %d일"),
            "HOME_NM": match.HOME_NM, 
            "AWAY_NM": match.AWAY_NM,
            "HOME_SCORE": row.HOME_SCORE if row.HOME_NM == match.HOME_NM else row.AWAY_SCORE,
            "AWAY_SCORE": row.AWAY_SCORE if row.AWAY_NM == match.AWAY_NM else row.HOME_SCORE,
        })
    
    home = [row for row in rank if row.TEAM_NM == match.HOME_NM][0]
    away = [row for row in rank if row.TEAM_NM == match.AWAY_NM][0]

    return jsonify({
        "SEASON_ID": match.SEASON_ID,
        "S_NM": match.S_NM,
        "G_DT_TXT": match.G_DT_TXT,
        "TV_IF": match.TV_IF,
        "HOME_ID": match.HOME_ID,
        "HOME_NM": team[match.HOME_ID]["full"],
        "HOME_SCORE": f"{home.W_CN}승 {home.D_CN}무 {home.L_CN}패 ( {home.RANK}위 )",
        "HOME_COLOR": team[match.HOME_ID]["color"],
        "AWAY_ID": match.AWAY_ID,
        "AWAY_NM": team[match.AWAY_ID]["full"],
        "AWAY_SCORE": f"{away.W_CN}승 {away.D_CN}무 {away.L_CN}패 ( {away.RANK}위 )",
        "AWAY_COLOR": team[match.AWAY_ID]["color"],
        "OP_SCORE": [int(op_rank.W_CN), int(op_rank.D_CN), int(op_rank.L_CN)],
        "SS_OP_SCORE": [int(ss_op_rank.W_CN), int(ss_op_rank.D_CN), int(ss_op_rank.L_CN)],
        "MATCH_SCORE": matches,
        "H_HITTER_INFO": [int(home_hitter["R"]), 
                     int(home_hitter["H"]), 
                     int(home_hitter["HR"]), 
                     int(home_hitter["RBI"]), 
                     int(home_hitter["2B"]), 
                     int(home_hitter["3B"]), 
                     int(home_hitter["BB"]), 
                     int(home_hitter["SO"])],
        "A_HITTER_INFO": [int(away_hitter["R"]), 
                     int(away_hitter["H"]), 
                     int(away_hitter["HR"]), 
                     int(away_hitter["RBI"]), 
                     int(away_hitter["2B"]), 
                     int(away_hitter["3B"]), 
                     int(away_hitter["BB"]), 
                     int(away_hitter["SO"])]
    })

@APP.route("/")
def index():
    return render_template("index.html", games=fetch_game_list(), home_color="#000000", away_color="#0072CE") 

if __name__ == "__main__":
    APP.run(debug=True)
