from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "ksdjflakjdflksjfll"


@app.route("/")
def home():
    return render_template("home.html", name="Mais")  # passing variable to page


@app.route("/about")
def about():
    return "<h2>this is url shortner </h2>"


# request.args["code"] for get info from request
# code=request.args["code"] ONLY FOR GET REQUESTS
# for posts methods code=request.form["code"]
# for posts methods code=request.form.get("code")
@app.route("/yoururl", methods=["GET", "POST"])
def your_url():  # sourcery skip: merge-dict-assign
    if request.method != "POST":
        return redirect(url_for("home"))  # redirect with url_for should give function
    url = {}
    if os.path.exists("ursls.json"):
        with open("ursls.json") as jfile:
            url = json.load(jfile)

    if request.form["code"] in url.keys():  # created dictionary
        flash("the shortname already been taken.")
        return redirect(url_for("home"))
    if "url" in request.form.keys():
        url[request.form["code"]] = {"url": request.form["url"]}
    else:
        f = request.files["file"]
        full_name = request.form["code"] + secure_filename(f.filename)
        f.save("E:\\learned\\flask_linkedin\\url-shortner\\app.py\\" + full_name)
        url[request.form["code"]] = {"file": full_name}

    with open("ursls.json", "w") as jfile:
        json.dump(url, jfile)

    return render_template(
        "yoururl.html", code=request.form["code"], whole=request.form
    )
    # but if it is only redirect need to giv app.route slash item>> '/'


# E:\\learned\\flask_linkedin\\url-shortner\\app.py

# redirect to rout app
# redirect("/")  redirect to rout app


if __name__ == "__main__":
    app.run(debug=True)
# python app.py
