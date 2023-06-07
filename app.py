from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", name="<h2>Mais<h2>")  # passing variable to page


@app.route("/about")
def about():
    return "<h2>this is url shortner </h2>"


# request.args["code"] for get info from request
# code=request.args["code"] ONLY FOR GET REQUESTS
# for posts methods code=request.form["code"]
# for posts methods code=request.form.get("code")
@app.route("/yoururl", methods=["GET", "POST"])
def your_url():
    if request.method == "POST":
        return render_template("yoururl.html", code=request.form["code"])
    else:
        return redirect(url_for("home"))  # redirect to function


# redirect to rout app
# redirect("/")  redirect to rout app

if __name__ == "__main__":
    app.run()
# python app.py
