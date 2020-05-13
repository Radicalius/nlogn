import flask, os
from flask import Flask, render_template, send_file

template_dir = os.path.abspath("html")
app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def index():
    return render_template("base.html", page="index.html")

@app.route("/articles/<name>")
def article(name):
    return render_template("base.html", page="index.html")

@app.route("/css/<file>")
def style(file):
    return send_file("css/"+file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
