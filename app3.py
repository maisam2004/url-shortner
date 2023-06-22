from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    session,
    jsonify,
)
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "ksdjflakjdflksjfll"
UPLOAD_FOLDER = "E:\\learned\\flask_linkedin\\url-shortner\\static\\user_files\\"


@app.route("/")
def home():
    return render_template("home.html", codes=session.keys())


@app.route("/about")
def about():
    return "<h2>This is URL shortener</h2>"


@app.route("/notfound")
def notfound():
    return render_template("page_not_find.html")


@app.route("/yoururl", methods=["GET", "POST"])
def your_url():
    if request.method != "POST":
        return redirect(url_for("home"))

    url = {}

    if os.path.exists("ursls.json"):
        with open("ursls.json") as jfile:
            url = json.load(jfile)

    code = request.form["code"]

    if code in url:
        flash("The shortname has already been taken.")
        return redirect(url_for("home"))

    if "url" in request.form:
        url[code] = {"url": request.form["url"]}
    else:
        f = request.files["file"]
        full_name = code + secure_filename(f.filename)
        save_path = os.path.join(UPLOAD_FOLDER, full_name)
        f.save(save_path)
        url[code] = {"file": full_name}

    with open("ursls.json", "w") as jfile:
        json.dump(url, jfile)
        session[code] = True

    return render_template("yoururl.html", code=code, whole=request.form)


@app.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists("ursls.json"):
        with open("ursls.json") as jfile:
            urls = json.load(jfile)
        if code in urls:
            if "url" in urls[code]:
                return redirect(urls[code]["url"])
            elif "file" in urls[code]:
                return redirect(
                    url_for("static", filename="user_files/" + urls[code]["file"])
                )
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_find.html"), 404


@app.route("/api")
def session_api():
    return jsonify(list(session.keys()))


if __name__ == "__main__":
    app.run(debug=True)
