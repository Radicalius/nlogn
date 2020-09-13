import flask
from flask import Flask, request
import requests
import sys, os
import redis

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import Crypto.Signature.pkcs1_15
import base64

def verify(publickey,data,sign):
    hash = SHA256.new(data.encode("utf8"))
    signer = Crypto.Signature.pkcs1_15.new(RSA.import_key(publickey))
    try:
        signer.verify(hash, base64.b64decode(sign))
        return True
    except ValueError:
        return False

app = Flask(__name__, template_folder=".")
r = redis.Redis.from_url(os.environ["REDIS_URL"])

@app.route("/<domain>/<file>", methods=["GET"])
def get(domain, file):
    resp = r.get(domain+"/"+file)
    if not resp:
        return "", 404
    return resp, 200

@app.route("/<domain>/<file>", methods=["POST", "PUT"])
def post(domain, file):
    pub_key = r.get(domain+"/key.pub")
    json = request.get_json()
    if not verify(pub_key, json["content"], json["signature"]):
        return "", 401
    if request.method == "POST":
        r.set(domain+"/"+file, json["content"])
    else:
        r.append(domain+"/"+file, json["content"])
    return "", 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
