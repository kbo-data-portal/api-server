from flask import Blueprint, request, jsonify

import re
from datetime import datetime, timedelta

from fetcher.game import (
    fetch_game_prediction
)

from constants import TEAMS

chatbot_bp = Blueprint("chatbot_bp", __name__)

def _get_template(output):
    return {
        "version": "2.0",
        "template": {
            "outputs": [output]
        }
    }

def _get_error_template(output):
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": output
                    }
                }
            ]
        }
    }

def _get_date(params):
    weekday = ["월", "화", "수", "목", "금", "토", "일"]
    today = datetime.today()
    
    text = ""
    for key in ["date", "date1", "date2"]:
        if key in params:
            text += str(params[key]["origin"])

    if "오늘" in text:
        return today
    elif "내일" in text:
        return today + timedelta(days=1)
    elif "어제" in text:
        return today - timedelta(days=1)
    elif "모레" in text:
        return today + timedelta(days=2)
    elif "그제" in text:
        return today - timedelta(days=2)

    date_match = re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", text)
    if date_match:
        y, m, d = map(int, date_match.groups())
        return datetime(year=y, month=m, day=d)
    
    kor_date_match = re.search(r"(\d{1,2})월\s*(\d{1,2})일", text)
    if kor_date_match:
        m, d = map(int, kor_date_match.groups())
        return datetime(year=today.year, month=m, day=d)

    if "다음" in text and "주" in text:
        for i, d in enumerate(weekday):
            if d in text:
                days = i - today.weekday() + 7
                return today + timedelta(days=days)
        days = 1 - today.weekday() + 7
        return today + timedelta(days=days)

    for i, d in enumerate(weekday):
        if d in text:
            days = i - today.weekday()
            return today + timedelta(days=days)
            
    return None

def _get_team(params):
    team_mapping = {
        "키움": ["키움", "히어로즈"],
        "두산": ["두산", "베어스"],
        "롯데": ["롯데", "자이언츠"],
        "삼성": ["삼성", "라이온즈"],
        "한화": ["한화", "이글스"],
        "KIA": ["KIA", "타이거즈"],
        "LG": ["LG", "트윈스"],
        "SSG": ["SSG", "랜더스"],
        "NC": ["NC", "다이노스"],
        "KT": ["KT", "위즈"],
    }
    
    text = ""
    for key in ["team", "team1"]:
        if key in params:
            text += str(params[key]["origin"])

    for name, keywords in team_mapping.items():
        for keyword in keywords:
            if keyword in text.upper():
                return name

def _get_proba(game):
    team = game.HOME_NM if game.HOME_WIN else game.AWAY_NM
    prob = game.HOME_WIN_PROB if game.HOME_WIN else game.AWAY_WIN_PROB
    percent = int(prob * 100)

    if percent >= 95:
        descriptor = "압도적 우세"
    elif percent >= 75:
        descriptor = "우세"
    elif percent >= 55:
        descriptor = "근소 우세"
    else:
        return game.HOME_NM, "접전 예상"

    return team, f"{team} {descriptor} (승리 {percent}%)"

def _get_stat_comparison(home_nm, away_nm, home_stat, away_stat, convert=False, reverse=False):
    if convert:
        home_stat = int(home_stat)
        away_stat = int(away_stat)
    if reverse:
        home_stat = round(home_stat, 2)
        away_stat = round(away_stat, 2)
        return f"{away_nm}({away_stat}) {"🔼" if away_stat < home_stat else ""} vs {home_nm}({home_stat}) {"🔼" if home_stat < away_stat else ""}"
    return f"{away_nm}({away_stat}) {"🔼" if away_stat > home_stat else ""} vs {home_nm}({home_stat}) {"🔼" if home_stat > away_stat else ""}"


@chatbot_bp.route("/schedule", methods=["POST"])
def schedule():
    data = request.get_json()
    params = data["action"]["detailParams"]

    request_date = _get_date(params)
    if not request_date:
        return jsonify(_get_error_template(
            "입력하신 날짜 형식을 이해하지 못했습니다.\n예: '오늘 경기 알려줘', '다음 주 금요일 일정 알려줘'처럼 입력해 주세요."
        ))
    
    game_schedule = fetch_game_prediction(date=request_date)

    items = []
    for schedule in game_schedule[:5]:
        team, proba = _get_proba(schedule)
        description =  f"{schedule.G_TM} · {proba}"

        if schedule.GAME_RESULT_CK == 1 or schedule.RESULT is not None:
            if schedule.AWAY_SCORE > schedule.HOME_SCORE:
                result = f"{schedule.AWAY_NM} 승"
            elif schedule.AWAY_SCORE < schedule.HOME_SCORE:
                result = f"{schedule.HOME_NM} 승"
            else:
                result = "무승부"
            description = f"{schedule.AWAY_SCORE} : {schedule.HOME_SCORE} · {result}"

        items.append({
            "title": f"{schedule.AWAY_NM} vs {schedule.HOME_NM} - {schedule.S_NM}",
            "description": description,
            "imageUrl": TEAMS[team]["logo"],
            "action": "block",
            "blockId": "682822d64df7f67fcdd445fe",
            "extra": {
                "date": { "origin": schedule.G_DT_TXT },
                "team": { "origin": schedule.HOME_NM }
            }
        })
        
    if not items:
        return jsonify(_get_error_template(
            f"{request_date.strftime('%m월 %d일')}에는 예정된 경기가 없습니다.\n다른 날짜를 선택해 주세요."
        ))

    return jsonify(_get_template(
        {
            "listCard": {
                "header": {
                  "title": f"📅 {request_date.strftime("%m월 %d일")} 경기 일정"
                },
                "items": items, 
                "buttons": [
                  {
                    "label": "경기 정보 더 보기",
                    "action": "webLink",
                    "webLinkUrl": f"https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={request_date.strftime("%Y%m%d")}"
                  }
                ]
            }
        }
    ))


@chatbot_bp.route("/team_schedule", methods=["POST"])
def team_schedule():
    data = request.get_json()
    params = data["action"]["detailParams"]
    
    request_date = _get_date(params)
    request_team = _get_team(params)
    if not request_team:
        return jsonify(_get_error_template(
            "입력하신 팀 이름을 이해하지 못했습니다.\n예: '삼성 경기 일정 알려줘', '내일 삼성 경기 알려줘'처럼 입력해 주세요."
        ))
    
    game_schedule = fetch_game_prediction(request_date, request_team)

    items = []
    for schedule in game_schedule[:5]:
        team = schedule.AWAY_NM if schedule.HOME_NM == request_team else schedule.HOME_NM

        items.append({
            "title": f"vs {TEAMS[team]["full"]} - {schedule.S_NM}",
            "description": f"{schedule.G_DT_TXT} {schedule.G_TM}",
            "imageUrl": TEAMS[team]["logo"],
            "action": "block",
            "blockId": "682822d64df7f67fcdd445fe",
            "extra": {
                "date": { "origin": schedule.G_DT_TXT },
                "team": { "origin": request_team }
            }
        })
        
    if not items:
        return jsonify(_get_error_template(
            f"죄송합니다. {request_team}의 예정된 경기가 없습니다."
        ))

    return jsonify(_get_template(
        {
            "listCard": {
                "header": {
                  "title": f"⚾ {TEAMS[request_team]["full"]} 경기 일정"
                },
                "items": items, 
            }
        }
    ))


@chatbot_bp.route("/game_detail", methods=["POST"])
def game_detail():
    data = request.get_json()
    params = data["action"]["clientExtra"]

    request_date = _get_date(params)
    request_team = _get_team(params)
    if not request_date:
        return jsonify(_get_error_template(
            "입력하신 날짜 형식을 이해하지 못했습니다.\n예: '오늘 경기 알려줘', '다음 주 금요일 일정 알려줘'처럼 입력해 주세요."
        ))
    if not request_team:
        return jsonify(_get_error_template(
            "입력하신 팀 이름을 이해하지 못했습니다.\n예: '삼성 경기 일정 알려줘', '내일 삼성 경기 알려줘'처럼 입력해 주세요."
        ))
    
    
    game = fetch_game_prediction(request_date, request_team)[0]
    team, proba = _get_proba(game)

    card = {
            "title": f"{TEAMS[game.AWAY_NM]["full"]} vs {TEAMS[game.HOME_NM]["full"]}",
            "description": (
                f"장소: {game.S_NM} · 일시: {game.G_DT.strftime("%m월 %d일")} {game.G_TM}\n\n"
                f"🏆 예상 승리 확률\n"
                f"- {TEAMS[game.AWAY_NM]["full"]}: {round(game.AWAY_WIN_PROB * 100, 2)}% {"🔼" if game.AWAY_NM == team else ""}\n"
                f"- {TEAMS[game.HOME_NM]["full"]}: {round(game.HOME_WIN_PROB * 100, 2)}% {"🔼" if game.HOME_NM == team else ""}\n\n"
                f"⚾️ 팀 투수 비교\n"
                f"- ERA: {_get_stat_comparison(game.HOME_NM, game.AWAY_NM, game.HOME_ERA, game.AWAY_ERA, False, True)}\n"
                f"- 탈삼진: {_get_stat_comparison(game.HOME_NM, game.AWAY_NM, game.HOME_PSO, game.AWAY_PSO, True)}\n\n"
                f"🔥 팀 타자 비교\n"
                f"- 타율: {_get_stat_comparison(game.HOME_NM, game.AWAY_NM, game.HOME_AVG, game.AWAY_AVG)}\n"
                f"- 홈런: {_get_stat_comparison(game.HOME_NM, game.AWAY_NM, game.HOME_HR, game.AWAY_HR, True)}\n"
            ),
            "thumbnail": {
                "imageUrl": TEAMS[team]["logo"],
            },
            "buttons": [
                {
                    "label": "경기 정보 자세히 보기",
                    "action": "webLink",
                    "webLinkUrl": f"https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={game.G_DT}&gameId=gameDate={game.G_ID}&section=REVIEW"
                }
            ]
        }

    return jsonify(_get_template(
        {
            "basicCard": card
        }
    ))

