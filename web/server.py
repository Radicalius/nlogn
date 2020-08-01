import flask, os, json, sys, requests
from flask import Flask, render_template, send_file
from mdparser import *
from threading import Timer

template_dir = os.path.abspath("html")
app = Flask(__name__, template_folder=template_dir)

md = {}
def caching_render_html(file):
    if file in md:
        return md[file]
    else:
        md[file] = render_html(file)
        return md[file]

mf = json.load(open("markdown/manifest.json"))

@app.route("/")
def index():
    return render_template("base.html", markdown=False, page="index.html", posts=mf["files"])

@app.route("/<t>")
def computing(t):
    if t not in ["music", "computing", "datascience"]:
        return "404 Error: Page Not Found", 404
    return render_template("base.html", type=t.capitalize(), markdown=False, page="index.html", posts=[i for i in mf["files"] if t in i["tags"]])

@app.route("/articles/<name>")
def article(name):
    return render_template("base.html", content=render_html("markdown/"+name+".md"), markdown=True)

@app.route("/css/<file>")
def style(file):
    return send_file("css/"+file)

@app.route("/scripts/<file>")
def script(file):
    return send_file("scripts/"+file)

@app.route("/img/<img>")
def image(img):
    return send_file("img/"+img)

def wake_up():
    requests.get("http://www.nlogn.blog")
    Timer(60, wake_up).start()

if __name__ == "__main__":
    Timer(60, wake_up).start()
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
