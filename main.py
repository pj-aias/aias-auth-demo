import platform

import ctypes
from ctypes import cdll, c_char_p, c_int32

def main():
    lib = get_lib()

    with open("parameters/signature.txt", 'rb') as f:
        signature = f.read()
    with open("parameters/message.txt", 'rb') as f:
        message = f.read()
    with open("parameters/signer_pubkey.pem", 'rb') as f:
        signer_pubkey = f.read()
    with open("parameters/judge_pubkey.pem", 'rb') as f:
        judge_pubkey = f.read()

    lib.verify.restype = c_int32

    res = lib.verify(signature, message, signer_pubkey, judge_pubkey)

    print(f"verify result: {bool(res)}")

def get_lib():
    pf = platform.system()
    if pf == 'Darwin':
        return cdll.LoadLibrary("aias-core/ffi/target/release/liblib.dylib")
    elif pf == 'Linux':
        return cdll.LoadLibrary("aias-core/ffi/target/release/liblib.so")


if __name__ == "__main__":
    main()