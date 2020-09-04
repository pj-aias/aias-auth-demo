import os
import random

import platform
import base64
import json

import ctypes
from ctypes import cdll, c_char_p, c_int32

from flask import Flask, request, json, jsonify, session

app = Flask(__name__)
app.secret_key = "akakouhaunko"

def verify_signature(data):
    lib = get_lib()

    with open("parameters/message.txt", 'rb') as f:
        message = f.read()
    with open("parameters/signer_pubkey.pem", 'rb') as f:
        signer_pubkey = f.read()
    with open("parameters/judge_pubkey.pem", 'rb') as f:
        judge_pubkey = f.read()

    lib.verify.restype = c_int32
    lib.verify.argtypes = (c_char_p, c_char_p, c_char_p)

    return lib.verify(data, signer_pubkey, judge_pubkey)

def verify_token(session, body):
    print("session:", session)
    try:
        data = json.loads(body)
        v = session['token'] == data['signed']['random']
        return v
    except Exception as e:
        print(f"error: {e}")
        return False

@app.route('/get', methods=['GET'])
def get():
    dataFile = open('data.txt', 'r') 
    lines = dataFile.readlines()
    lines = list(map(lambda line: line.rstrip('\n'), lines))

    resp = {'data':lines}
    return json.dumps(resp)

@app.route('/post', methods=['POST'])
def index():
    valid_sig = verify_signature(request.get_data())
    valid_token = verify_token(session, request.get_data())
    valid = valid_sig and valid_token

    reqJson = json.loads(request.get_data())

    resp = {
        "result": bool(valid)
    }

    if valid:
        print(reqJson['fair_blind_signature'])
        with open('data.txt', 'a') as f:
            print(reqJson["signed"]["data"], file=f)
        random_token = get_random_token()

        resp['random'] = str(random_token)
        session['token'] = random_token

    return json.dumps(resp)

@app.route('/token', methods=['POST'])
def token():
    resp = {}

    random_token = get_random_token()
    resp['random'] = str(random_token)
    session['token'] = random_token

    return json.dumps(resp)

def get_random_token():
    if app.debug == True:
        return 111111
    else:
        rng = random.SystemRandom()
        random_token = rng.randint(100000, 999999)
        return random_token

def get_lib():
    pf = platform.system()
    if pf == 'Darwin':
        return cdll.LoadLibrary("aias-auth-sdk/ffi/target/release/liblib.dylib")
    elif pf == 'Linux':
        return cdll.LoadLibrary("aias-auth-sdk/ffi/target/release/liblib.so")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
