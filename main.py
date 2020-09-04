import platform
import base64
import json

import ctypes
from ctypes import cdll, c_char_p, c_int32

from flask import Flask, request, json, jsonify

app = Flask(__name__)

def verify(data):
    lib = get_lib()

    with open("parameters/message.txt", 'rb') as f:
        message = f.read()
    with open("parameters/signer_pubkey.pem", 'rb') as f:
        signer_pubkey = f.read()
    with open("parameters/judge_pubkey.pem", 'rb') as f:
        judge_pubkey = f.read()

    print(judge_pubkey)

    lib.verify.restype = c_int32
    lib.verify.argtypes = (c_char_p, c_char_p, c_char_p)

    return lib.verify(data, signer_pubkey, judge_pubkey)

@app.route('/verify', methods=['POST'])
def index():
    is_valid = verify(request.get_data())

    resp = {
        "result": bool(is_valid)
    }
    return json.dumps(resp)


def get_lib():
    pf = platform.system()
    if pf == 'Darwin':
        return cdll.LoadLibrary("aias-auth-sdk/ffi/target/release/liblib.dylib")
    elif pf == 'Linux':
        return cdll.LoadLibrary("aias-auth-sdk/ffi/target/release/liblib.so")


if __name__ == "__main__":
    app.run()
