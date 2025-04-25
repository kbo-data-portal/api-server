from flask import Flask, render_template, request, jsonify
from fetcher import (
    fetch_recent_games,
    fetch_game_info_by_id,
    fetch_team_rankings,
    fetch_vs_team_stats,
    fetch_head_to_head_recent_games,
    fetch_team_hitting_stats,
    fetch_team_pitching_stats,
    fetch_player_hitting_stats,
    fetch_player_pitching_stats,
)
from datetime import datetime

APP = Flask(__name__)
TEAMS = {
    "키움": { "id": "WO", "full": "키움 히어로즈", "color": "#570514" },
    "두산": { "id": "OB", "full": "두산 베어스", "color": "#1A1748" },
    "롯데": { "id": "LT", "full": "롯데 자이언츠", "color": "#041E42" },
    "삼성": { "id": "SS", "full": "삼성 라이온즈", "color": "#074CA1" },
    "한화": { "id": "HH", "full": "한화 이글스", "color": "#FC4E00" },
    "KIA": { "id": "HT", "full": "KIA 타이거즈", "color": "#EA0029" },
    "LG": { "id": "LG", "full": "LG 트윈스", "color": "#C30452" },
    "SSG": { "id": "SK", "full": "SSG 랜더스", "color": "#CE0E2D" },
    "NC": { "id": "NC", "full": "NC 다이노스", "color": "#315288" },
    "KT": { "id": "KT", "full": "KT 위즈", "color": "#000000" },
    None: { "id": "NO", "full": "없음", "color": "#002063" }
}


@APP.route("/get_team_players", methods=["POST"])
def get_team_players():
    data = request.get_json()
    team_name = data.get("team_name")
    
    hitter_ranks = fetch_player_hitting_stats(datetime.now().year, team_name)
    hitters = []
    for hitter in hitter_ranks[:5]:
        hitters.append({
            "team_id": TEAMS[hitter.TEAM_NM]["id"],
            "team": TEAMS[hitter.TEAM_NM]["full"],
            "player_id": hitter.P_ID,
            "name": hitter.P_NM,
            "data": [f"{hitter.AVG:.3f}", hitter.R, hitter.H],
            "rank": hitter.RANK
        })

    pitcher_ranks = fetch_player_pitching_stats(datetime.now().year, team_name)
    pitchers = []
    for pitcher in pitcher_ranks[:5]:
        pitchers.append({
            "team_id": TEAMS[pitcher.TEAM_NM]["id"],
            "team": TEAMS[pitcher.TEAM_NM]["full"],
            "player_id": pitcher.P_ID,
            "name": pitcher.P_NM,
            "data": [f"{pitcher.ERA:.2f}", pitcher.W, pitcher.SO],
            "rank": pitcher.RANK
        })

    return jsonify({
        "hitter": hitters,
        "pitcher": pitchers,
        "color": TEAMS[team_name]["color"],
    })


@APP.route("/get_team_stats", methods=["POST"])
def get_team_stats_by_type():
    data = request.get_json()
    player_type = data.get("player_type")

    season_id = data.get("season_id")
    home_name = data.get("home_name")
    away_name = data.get("away_name")
    
    if player_type == "hitter":
        columns = ["R", "H", "HR", "RBI", "2B", "3B", "BB", "SO"]
        stat_columns = ["득점", "안타", "홈런", "타점", "2루타", "3루타", "볼넷", "삼진"]
        home_stats_raw = fetch_team_hitting_stats(season_id, home_name)
        away_stats_raw = fetch_team_hitting_stats(season_id, away_name)
    elif player_type == "pitcher":
        columns = ["W", "L", "SO", "BB", "SV", "HLD", "H", "ER"]
        stat_columns = ["승리", "패배", "삼진", "볼넷", "세이브", "홀드", "피안타", "자책점"]
        home_stats_raw = fetch_team_pitching_stats(season_id, home_name)
        away_stats_raw = fetch_team_pitching_stats(season_id, away_name)
    else:
        return jsonify({"error": "Invalid player type"}), 400

    home_stats, away_stats = [], []
    for column in columns:
        home_stats.append(int(home_stats_raw[column]))
        away_stats.append(int(away_stats_raw[column]))

    return jsonify({
        "columns": stat_columns,
        "home_team_stats": home_stats,
        "home_team_color": TEAMS[home_name]["color"],
        "away_team_stats": away_stats,
        "away_team_color": TEAMS[away_name]["color"],
    })


@APP.route("/get_match", methods=["POST"])
def get_match_info():
    data = request.get_json()
    game_id = data.get("game_id")

    match_info = fetch_game_info_by_id(game_id)
    team_ranks = fetch_team_rankings(match_info.SEASON_ID)

    home_overall_vs_rank = fetch_vs_team_stats(0, match_info.HOME_NM, match_info.AWAY_NM)
    home_season_vs_rank = fetch_vs_team_stats(match_info.SEASON_ID, match_info.HOME_NM, match_info.AWAY_NM)
    away_overall_vs_rank = fetch_vs_team_stats(0, match_info.AWAY_NM, match_info.HOME_NM)
    away_season_vs_rank = fetch_vs_team_stats(match_info.SEASON_ID, match_info.AWAY_NM, match_info.HOME_NM)

    recent_match_results = fetch_head_to_head_recent_games(match_info.HOME_NM, match_info.AWAY_NM)

    match_summary_list = []
    for row in recent_match_results:
        match_summary_list.append({
            "game_date": datetime.strptime(row.G_DT, "%Y-%m-%d").strftime("%Y년 %m월 %d일"),
            "home_team_name": match_info.HOME_NM,
            "away_team_name": match_info.AWAY_NM,
            "home_team_score": row.HOME_SCORE if row.HOME_NM == match_info.HOME_NM else row.AWAY_SCORE,
            "away_team_score": row.AWAY_SCORE if row.AWAY_NM == match_info.AWAY_NM else row.HOME_SCORE,
        })

    home_rank = next(row for row in team_ranks if row.TEAM_NM == match_info.HOME_NM)
    away_rank = next(row for row in team_ranks if row.TEAM_NM == match_info.AWAY_NM)

    return jsonify({
        "season_id": match_info.SEASON_ID,
        "stadium_name": match_info.S_NM,
        "game_date": match_info.G_DT_TXT,
        "tv_channel": match_info.TV_IF,
        "home_team_id": match_info.HOME_ID,
        "home_team_name": match_info.HOME_NM,
        "home_team_full_name": TEAMS[match_info.HOME_NM]["full"],
        "home_team_color": TEAMS[match_info.HOME_NM]["color"],
        "home_team_record": f"{home_rank.W_CN}승 {home_rank.D_CN}무 {home_rank.L_CN}패 ( {home_rank.RANK}위 )",
        "away_team_id": match_info.AWAY_ID,
        "away_team_name": match_info.AWAY_NM,
        "away_team_full_name": TEAMS[match_info.AWAY_NM]["full"],
        "away_team_color": TEAMS[match_info.AWAY_NM]["color"],
        "away_team_record": f"{away_rank.W_CN}승 {away_rank.D_CN}무 {away_rank.L_CN}패 ( {away_rank.RANK}위 )",
        "overall_vs_record": [int(home_overall_vs_rank.W_CN), int(home_overall_vs_rank.D_CN), int(away_overall_vs_rank.W_CN), int(home_overall_vs_rank.R), int(away_overall_vs_rank.R)],
        "season_vs_record": [int(home_season_vs_rank.W_CN), int(home_season_vs_rank.D_CN), int(away_season_vs_rank.W_CN), int(home_season_vs_rank.R), int(away_season_vs_rank.R)],
        "recent_match_results": match_summary_list
    })


@APP.route("/")
def index():
    return render_template("index.html", 
                           games=fetch_recent_games(), 
                           ranks=fetch_team_rankings(datetime.now().year))

if __name__ == "__main__":
    APP.run(debug=True)
