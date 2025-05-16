from flask import Blueprint, request, jsonify

import re
from datetime import datetime, timedelta

from fetcher.game import (
    fetch_game_schedule_by_date
)

chatbot_bp = Blueprint("chatbot_bp", __name__)

def _get_template(output):
    return {
        "version": "2.0",
        "template": {
            "outputs": [output]
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

    teams = []
    for name, keywords in team_mapping.items():
        for keyword in keywords:
            if keyword in text.upper():
                teams.append(name)
                break
            
    return teams


@chatbot_bp.route("/schedule", methods=["GET"])
def schedule():
    # data = request.get_json()
    # params = data["action"]["detailParams"]
    params = {
        "team": "ssg",
        "team1": "키움"
    }
    
    request_date = _get_date(params)
    request_team = _get_team(params)
    print(request_team)
    
    game_schedule = fetch_game_schedule_by_date(request_date, request_team)
    items = [
        {
            "title": f"{schedule.HOME_NM} vs {schedule.AWAY_NM}",
            "description": f"{schedule.S_NM} | {schedule.G_TM} | {schedule.G_DT_TXT}",
            "imageUrl": f"https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/KBOHome/resources/images/emblem/regular/{schedule.SEASON_ID}/emblem_{schedule.HOME_ID}.png",
            "link": {
                "web": f"https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={schedule.G_DT}&gameId=gameDate={schedule.G_ID}&section=REVIEW"
            }
        }
        for schedule in game_schedule[:5]
    ]

    return jsonify(_get_template(
        {
            "listCard": {
                "header": {
                  "title": "KBO 경기 정보가 도착했어요! ⚾"
                },
                "items": items, 
            }
        }
    ))


@chatbot_bp.route("/predict", methods=["POST"])
def predict_game():
    # data = request.get_json()
    # params = data["action"]["detailParams"]
    params = {
        "team": "ssg",
        "team1": "키움"
    }
    
    request_date = _get_date(params)
    request_team = _get_team(params)
    print(request_team)
    
    game_schedule = fetch_game_schedule_by_date(request_date, request_team)
    items = [
        {
            "title": f"{schedule.HOME_NM} vs {schedule.AWAY_NM}",
            "description": f"{schedule.S_NM} | {schedule.G_TM} | {schedule.G_DT_TXT}",
            "imageUrl": f"https://6ptotvmi5753.edge.naverncp.com/KBO_IMAGE/KBOHome/resources/images/emblem/regular/{schedule.SEASON_ID}/emblem_{schedule.HOME_ID}.png",
            "link": {
                "web": f"https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate={schedule.G_DT}&gameId=gameDate={schedule.G_ID}&section=REVIEW"
            }
        }
        for schedule in game_schedule[:5]
    ]

    return jsonify(_get_template(
        {
            "listCard": {
                "header": {
                  "title": "KBO 승부 예측이 도착했어요! ⚾"
                },
                "items": items, 
            }
        }
    ))

@chatbot_bp.route("/help", methods=["POST"])
def help():
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "KBO 챗봇 이용 가이드 🧾",
                        "description": (
                            "다음과 같은 질문을 할 수 있어요!\n\n"
                            "- 오늘 경기 알려줘\n"
                            "- LG 일정 알려줘\n"
                            "- 승부예측 보여줘"
                        ),
                        "buttons": [
                            {
                                "label": "오늘 경기",
                                "action": "block",
                                "blockId": "BLOCK_ID_TODAY"
                            },
                            {
                                "label": "승부예측",
                                "action": "block",
                                "blockId": "BLOCK_ID_PREDICT"
                            }
                        ]
                    }
                }
            ]
        }
    })

