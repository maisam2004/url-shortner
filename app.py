from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", name="Mais")  # passing variable to page


@app.route("/about")
def about():
    return "<h2>this is url shortner </h2>"


# request.args["code"] for get info from request
# code=request.args["code"] ONLY FOR GET REQUESTS
# for posts methods code=request.form.get["code"]
@app.route("/your_url", methods=["GET", "POST"])
def your_url():
    if request.method == "POST":
        return render_template("your_url.html", code=request.form.get("code"))
    else:
        return "This is not valid "


if __name__ == "__main__":
    app.run()
# python app.py
