import flask
from flask import Flask, render_template
import requests
import sys

app = Flask(__name__, template_folder=".")

@app.route("/to/<domain>")
def redirect(domain):
    return render_template("redirect.html", domain=domain)

@app.route("/check/<domain>")
def check(domain):
    try:
        requests.get("http://{0}.nlogn.blog".format(domain), timeout=2)
        return "", 200
    except:
        return "", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
