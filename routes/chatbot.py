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
            "simpleText": {
                "text": output
            }
        }
    }

def _get_date(params):
    weekday = ["월", "화", "수", "목", "금", "토", "일"]
    today = datetime.today()
    
    text = ""
    for key in ["date", "date1", "date2"]:
        if key in params:
            text += params[key]

    if "오늘" in text:
        return today
    elif "내일" in text:
        return today + timedelta(days=1)
    elif "모레" in text:
        return today + timedelta(days=2)

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
            text += params[key]

    for name, keywords in team_mapping.items():
        for keyword in keywords:
            if keyword in text.upper():
                return name

def _get_proba(game):
    team = game.HOME_NM if game.HOME_WIN else game.AWAY_NM
    prob = game.HOME_WIN_PROB if game.HOME_WIN else game.AWAY_WIN_PROB
    percent = round(prob * 100, 2)

    if percent >= 90:
        descriptor = "압도적 우세"
    elif percent >= 75:
        descriptor = "우세"
    elif percent >= 60:
        descriptor = "근소 우세"
    else:
        return game.HOME_NM, "접전 예상"

    return team, f"{team} {descriptor} (승리 확률 {percent}%)"


@chatbot_bp.route("/schedule", methods=["GET"])
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

        items.append({
            "title": f"{schedule.AWAY_NM} vs {schedule.HOME_NM} - {schedule.S_NM}",
            "description": f"{schedule.G_TM} · {proba}",
            "imageUrl": TEAMS[team]["logo"],
            "action": "block",
            "blockId": "test",
            "extra": {
              "date": request_date.strftime('%m월 %d일'),
              "team": schedule.HOME_NM
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
                    "webLinkUrl": f"https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={request_date.strftime('%Y%m%d')}"
                  }
                ]
            }
        }
    ))


@chatbot_bp.route("/team_schedule", methods=["GET"])
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
            "blockId": "test",
            "extra": {
              "date": request_date.strftime('%m월 %d일'),
              "team": request_team
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


@chatbot_bp.route("/help", methods=["POST"])
def help():
    return jsonify(_get_template(
        {
            "basicCard": {
                "title": "🧾 KBO 챗봇 이용 가이드",
                "description": (
                    "다음과 같은 질문을 할 수 있어요!\n\n"
                    "- 오늘 경기 알려줘\n"
                    "- 다음 주 금요일 일정 알려줘\n"
                    "- 4월 10일 경기 알려줘\n"
                    "- 삼성 경기 일정 알려줘\n"
                    "- 내일 삼성 경기 알려줘\n"
                ),
                "buttons": [
                    {
                        "label": "오늘 경기",
                        "action": "block",
                        "blockId": "BLOCK_ID_TODAY"
                    }
                ]
            }
        }
    ))

