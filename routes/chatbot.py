from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint("chatbot_bp", __name__)


@chatbot_bp.route('/today_schedule', methods=['POST'])
def today_schedule():
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "listCard": {
                        "header": {
                            "title": "오늘의 KBO 경기일정 ⚾"
                        },
                        "items": [
                            {
                                "title": "LG vs 두산",
                                "description": "잠실 | 18:30",
                                "imageUrl": "https://yourcdn.com/logo_lg_dosan.png"
                            },
                            {
                                "title": "삼성 vs KIA",
                                "description": "대구 | 18:30",
                                "imageUrl": "https://yourcdn.com/logo_samsung_kia.png"
                            }
                        ],
                        "buttons": [
                            {
                                "label": "내일 경기 보기",
                                "action": "block",
                                "blockId": "BLOCK_ID_TOMORROW"
                            }
                        ]
                    }
                }
            ]
        }
    })


@chatbot_bp.route('/predict_game', methods=['POST'])
def predict_game():
    team_a = "LG"
    team_b = "두산"
    prediction = "LG 승률 65%\n두산 승률 35%"

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": f"{team_a} vs {team_b} 승부예측",
                        "description": prediction,
                        "thumbnail": {
                            "imageUrl": "https://yourcdn.com/prediction_chart.png"
                        },
                        "buttons": [
                            {
                                "label": "다른 경기 예측",
                                "action": "block",
                                "blockId": "BLOCK_ID_PREDICT"
                            }
                        ]
                    }
                }
            ]
        }
    })


@chatbot_bp.route('/team_schedule', methods=['POST'])
def team_schedule():
    team = "LG"
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": "5월 16일 (목)",
                                "description": "vs 두산 @잠실 | 18:30",
                                "thumbnail": {
                                    "imageUrl": "https://yourcdn.com/game1.png"
                                }
                            },
                            {
                                "title": "5월 17일 (금)",
                                "description": "vs SSG @문학 | 18:30",
                                "thumbnail": {
                                    "imageUrl": "https://yourcdn.com/game2.png"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    })


@chatbot_bp.route('/help', methods=['POST'])
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

