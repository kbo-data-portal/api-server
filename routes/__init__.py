from routes.chatbot import chatbot_bp
from routes.web import web_bp


def register_routes(app):
    app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
    app.register_blueprint(web_bp, url_prefix="/web")
