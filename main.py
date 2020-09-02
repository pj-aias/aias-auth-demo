import ctypes
from ctypes import cdll, c_char_p, c_int32

def main():
    lib = cdll.LoadLibrary("aias-core/ffi/target/release/liblib.dylib")

    signature = c_char_p(b"hoge")
    message = c_char_p(b"fuga")
    signer_pubkey = c_char_p(b"piyo")
    judge_pubkeys = c_char_p(b"foo")

    lib.verify.restype = c_int32

    res = lib.verify(signature, message, signer_pubkey, judge_pubkeys)

    print(f"output: {res}")

if __name__ == "__main__":
    main()