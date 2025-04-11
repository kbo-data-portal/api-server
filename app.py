from flask import Flask, render_template, request, jsonify

APP = Flask(__name__)

@APP.route("/")
def index():
    return render_template("index.html")

@APP.route("/1")
def chart_data():
    return render_template("index.html")

if __name__ == "__main__":
    APP.run(host="0.0.0.0")
