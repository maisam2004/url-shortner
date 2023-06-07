from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", name="Mais")  # passing variable to page


@app.route("/about")
def about():
    return "<h2>this is url shortner </h2>"


if __name__ == "__main__":
    app.run()
# python app.py
