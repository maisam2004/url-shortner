from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    session,
)
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "ksdjflakjdflksjfll"

UPLOAD_FOLDER = "E:\\learned\\flask_linkedin\\url-shortner\\static\\user_files"
URLS_FILE = "urls.json"


@app.route("/")
def home():
    return render_template("home.html", codes=session.keys())


@app.route("/about")
def about():
    return "<h2>This is a URL shortener.</h2>"


@app.route("/notfound")
def notfound():
    return render_template("page_not_find.html")


@app.route("/yoururl", methods=["GET", "POST"])
def your_url():
    if request.method != "POST":
        return redirect(url_for("home"))

    urls = load_urls_from_file()
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

    save_urls_to_file(urls)
    session[code] = True

    return render_template("yoururl.html", code=code, whole=request.form)


@app.route("/<string:code>")
def redirect_to_url(code):
    urls = load_urls_from_file()

    if code in urls:
        if "url" in urls[code]:
            return redirect(urls[code]["url"])
        elif "file" in urls[code]:
            return redirect(
                url_for("static", filename="user_files/" + urls[code]["file"])
            )

    return abort(404)


@app.errorhandler(404)
def page_not_find(error):
    return render_template("page_not_find.html"), 404


def load_urls_from_file():
    if os.path.exists(URLS_FILE):
        with open(URLS_FILE) as jfile:
            return json.load(jfile)
    return {}


def save_urls_to_file(urls):
    with open(URLS_FILE, "w") as jfile:
        json.dump(urls, jfile)


if __name__ == "__main__":
    app.run(debug=True)


""" 
Here are the optimizations made in this version:

Moved the functions load_urls_from_file and save_urls_to_file to separate functions for better code organization and reusability.
Created constants UPLOAD_FOLDER and URLS_FILE for better code readability and maintainability.
Moved the loading of URLs from the JSON file to a separate function load_urls_from_file.
Moved the saving of URLs to the JSON file to a separate function save_urls_to_file.
Simplified the code by removing unnecessary comments and unused imports.
Combined the if statements to reduce nesting and improve code readability.
Used os.path.join to join file paths for better platform independence.
Removed the redundant check for file existence before reading from the URLs file in the redirect_to_url function.
These optimizations should make your code more efficient, readable, and maintainable.

"""
