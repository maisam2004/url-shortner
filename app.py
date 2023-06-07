from flask import Flask


app = Flask(__name__)


@app.route("/")
def home():
    return "hello flask"


@app.route("/about")
def about():
    return "<h2>this is url shortner </h2>"


if __name__ == "__main__":
    app.run()
