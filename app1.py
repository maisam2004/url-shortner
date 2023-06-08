from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "ksdjflakjdflksjfll"

URLS_FILE = "urls.json"
UPLOAD_FOLDER = "E:\\learned\\flask_linkedin\\url-shortner"


@app.route("/")
def home():
    return render_template("home.html", name="Mais")


@app.route("/about")
def about():
    return "<h2>This is a URL shortener.</h2>"


@app.route("/yoururl", methods=["GET", "POST"])
def your_url():
    if request.method != "POST":
        return redirect(url_for("home"))

    urls = {}
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE) as jfile:
            urls = json.load(jfile)

    code = request.form["code"]
    if code in urls:
        flash("The shortname is already taken.")
        return redirect(url_for("home"))

    if "url" in request.form:
        urls[code] = {"url": request.form["url"]}
    else:
        f = request.files["file"]
        full_name = code + secure_filename(f.filename)
        save_path = os.path.join(UPLOAD_FOLDER, full_name)
        f.save(save_path)
        urls[code] = {"file": full_name}

    with open(URLS_FILE, "w") as jfile:
        json.dump(urls, jfile)

    return render_template("yoururl.html", code=code, whole=request.form)


@app.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE) as jfile:
            urls = json.load(jfile)
        if code in urls and "url" in urls[code]:
            return redirect(urls[code]["url"])


if __name__ == "__main__":
    app.run(debug=True)
