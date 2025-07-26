from flask import Flask, render_template
from datetime import datetime

from routes import register_routes

from fetcher.analytics import fetch_team_rankings
from fetcher.game import fetch_recent_games

app = Flask(__name__)
register_routes(app)


@app.route("/")
def index():
    return render_template(
        "index.html",
        today=datetime.now().strftime("%Y%m%d"),
        games=fetch_recent_games(),
        ranks=fetch_team_rankings(datetime.now().year),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
