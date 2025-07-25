from flask import Blueprint, request, jsonify
from datetime import datetime

from fetcher.analytics import (
    fetch_team_rankings,
    fetch_vs_team_stats,
    fetch_vs_team_stats_by_season,
    fetch_team_hitting_stats,
    fetch_team_pitching_stats,
)
from fetcher.game import (
    fetch_game_info_by_id,
    fetch_head_to_head_recent_games,
)
from fetcher.player import (
    fetch_player_hitting_stats,
    fetch_player_pitching_stats,
)

from constants import TEAMS

web_bp = Blueprint("web_bp", __name__)


@web_bp.route("/team_players", methods=["POST"])
def team_players():
    data = request.get_json()
    team_name = data.get("team_name")
    current_year = datetime.now().year

    hitter_ranks = fetch_player_hitting_stats(current_year, team_name)
    hitters = [
        {
            "team_id": TEAMS[hitter.TEAM_NM]["id"],
            "team": TEAMS[hitter.TEAM_NM]["full"],
            "player_id": hitter.P_ID,
            "name": hitter.P_NM,
            "data": [f"{hitter.AVG:.3f}", hitter.R, hitter.H],
            "rank": hitter.RANK,
        }
        for hitter in hitter_ranks[:5]
    ]

    pitcher_ranks = fetch_player_pitching_stats(current_year, team_name)
    pitchers = [
        {
            "team_id": TEAMS[pitcher.TEAM_NM]["id"],
            "team": TEAMS[pitcher.TEAM_NM]["full"],
            "player_id": pitcher.P_ID,
            "name": pitcher.P_NM,
            "data": [f"{pitcher.ERA:.2f}", pitcher.W, pitcher.SO],
            "rank": pitcher.RANK,
        }
        for pitcher in pitcher_ranks[:5]
    ]

    return jsonify(
        {
            "hitter": hitters,
            "pitcher": pitchers,
            "color": TEAMS[team_name]["color"],
        }
    )


@web_bp.route("/team_stats", methods=["POST"])
def team_stats():
    data = request.get_json()
    player_type = data.get("player_type")
    season_id = data.get("season_id")
    home_name = data.get("home_name")
    away_name = data.get("away_name")

    if player_type == "hitter":
        columns = ["R", "H", "HR", "RBI", "2B", "3B", "BB", "SO"]
        stat_columns = [
            "득점",
            "안타",
            "홈런",
            "타점",
            "2루타",
            "3루타",
            "볼넷",
            "삼진",
        ]
        fetch_func = fetch_team_hitting_stats
    elif player_type == "pitcher":
        columns = ["W", "L", "SO", "BB", "SV", "HLD", "H", "ER"]
        stat_columns = [
            "승리",
            "패배",
            "삼진",
            "볼넷",
            "세이브",
            "홀드",
            "피안타",
            "자책점",
        ]
        fetch_func = fetch_team_pitching_stats
    else:
        return jsonify({"error": "Invalid player type"}), 400

    home_stats_raw = fetch_func(season_id, home_name)
    away_stats_raw = fetch_func(season_id, away_name)

    home_stats = [int(home_stats_raw[col]) for col in columns]
    away_stats = [int(away_stats_raw[col]) for col in columns]

    return jsonify(
        {
            "columns": stat_columns,
            "home_team_stats": home_stats,
            "home_team_color": TEAMS[home_name]["color"],
            "away_team_stats": away_stats,
            "away_team_color": TEAMS[away_name]["color"],
        }
    )


@web_bp.route("/match_info", methods=["POST"])
def match_info():
    data = request.get_json()
    game_id = data.get("game_id")

    match_info = fetch_game_info_by_id(game_id)
    team_ranks = fetch_team_rankings(match_info["SEASON_ID"])

    home_overall_vs = fetch_vs_team_stats(match_info["HOME_NM"], match_info["AWAY_NM"])
    home_season_vs = fetch_vs_team_stats_by_season(
        match_info["SEASON_ID"], match_info["HOME_NM"], match_info["AWAY_NM"]
    )
    away_overall_vs = fetch_vs_team_stats(match_info["AWAY_NM"], match_info["HOME_NM"])
    away_season_vs = fetch_vs_team_stats_by_season(
        match_info["SEASON_ID"], match_info["AWAY_NM"], match_info["HOME_NM"]
    )

    recent_matches = fetch_head_to_head_recent_games(
        match_info["HOME_NM"], match_info["AWAY_NM"]
    )

    recent_match_list = [
        {
            "game_date": datetime.strptime(row.G_DT, "%Y-%m-%d").strftime(
                "%Y년 %m월 %d일"
            ),
            "home_team_name": match_info["HOME_NM"],
            "away_team_name": match_info["AWAY_NM"],
            "home_team_score": (
                row.HOME_SCORE
                if row.HOME_NM == match_info["HOME_NM"]
                else row.AWAY_SCORE
            ),
            "away_team_score": (
                row.AWAY_SCORE
                if row.AWAY_NM == match_info["AWAY_NM"]
                else row.HOME_SCORE
            ),
        }
        for row in recent_matches
    ]

    home_rank = next(r for r in team_ranks if r.TEAM_NM == match_info["HOME_NM"])
    away_rank = next(r for r in team_ranks if r.TEAM_NM == match_info["AWAY_NM"])

    return jsonify(
        {
            "season_id": match_info["SEASON_ID"],
            "stadium_name": match_info["S_NM"],
            "game_date": match_info["G_DT_TXT"],
            "tv_channel": match_info["TV_IF"],
            "home_team_id": match_info["HOME_ID"],
            "home_team_name": match_info["HOME_NM"],
            "home_team_full_name": TEAMS[match_info["HOME_NM"]]["full"],
            "home_team_color": TEAMS[match_info["HOME_NM"]]["color"],
            "home_team_record": f"{home_rank.W_CN}승 {home_rank.D_CN}무 {home_rank.L_CN}패 ( {home_rank.RANK}위 )",
            "away_team_id": match_info["AWAY_ID"],
            "away_team_name": match_info["AWAY_NM"],
            "away_team_full_name": TEAMS[match_info["AWAY_NM"]]["full"],
            "away_team_color": TEAMS[match_info["AWAY_NM"]]["color"],
            "away_team_record": f"{away_rank.W_CN}승 {away_rank.D_CN}무 {away_rank.L_CN}패 ( {away_rank.RANK}위 )",
            "overall_vs_record": [
                int(home_overall_vs["W_CN"]),
                int(home_overall_vs["D_CN"]),
                int(away_overall_vs["W_CN"]),
                int(home_overall_vs["R"]),
                int(away_overall_vs["R"]),
            ],
            "season_vs_record": [
                int(home_season_vs["W_CN"]),
                int(home_season_vs["D_CN"]),
                int(away_season_vs["W_CN"]),
                int(home_season_vs["R"]),
                int(away_season_vs["R"]),
            ],
            "recent_match_results": recent_match_list,
        }
    )
