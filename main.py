import platform
import base64
import json

import ctypes
from ctypes import cdll, c_char_p, c_int32

from flask import Flask, request, json, jsonify

app = Flask(__name__)


@app.route('/verify', methods=['POST'])
def verify():
    lib = get_lib()

    print(type(request.json))
    signature_json = request.json['fbs_signature']
    print(type(signature_json))
    signature = json.dumps(signature_json).encode('utf-8')
    print(type(signature))

    with open("parameters/message.txt", 'rb') as f:
        message = f.read()
    with open("parameters/signer_pubkey.pem", 'rb') as f:
        signer_pubkey = f.read()
    with open("parameters/judge_pubkey.pem", 'rb') as f:
        judge_pubkey = f.read()

    lib.verify.restype = c_int32

    lib.verify.argtypes = (c_char_p, c_char_p, c_char_p, c_char_p)
    res = lib.verify(signature, message, signer_pubkey, judge_pubkey)
    res = bool(res)
    return f"Verify result: {str(res)}"


def get_lib():
    pf = platform.system()
    if pf == 'Darwin':
        return cdll.LoadLibrary("aias-core/ffi/target/release/liblib.dylib")
    elif pf == 'Linux':
        return cdll.LoadLibrary("aias-core/ffi/target/release/liblib.so")


def main():
    app.run()



if __name__ == "__main__":
    main()