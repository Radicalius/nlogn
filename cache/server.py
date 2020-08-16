import flask
from flask import Flask
import requests
import sys, os
import redis

app = Flask(__name__, template_folder=".")
r = redis.Redis.from_url(os.environ["REDIS_URL"])

@app.route("/<domain>/<file>", methods=["GET"])
def get(domain, file):
    resp = r.get(domain+"/"+file)
    if not resp:
        return "", 404
    return resp, 200

@app.route("/<domain>/<file>", methods=["POST"])
def post(domain, file):
    cont = requests.get("http://"+domain+".nlogn.blog/"+file, timeout=2).text
    r.set(domain+"/"+file, cont)
    return "", 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
