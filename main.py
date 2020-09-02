import ctypes
from ctypes import cdll, c_char_p, c_int32

def main():
    lib = cdll.LoadLibrary("aias-core/ffi/target/release/liblib.dylib")

    a = c_char_p(b"hoge")
    b = c_char_p(b"fuga")
    c = c_char_p(b"piyo")
    d = c_char_p(b"foo")

    lib.verify.restype = c_int32

    lib.verify(a, b, c, d)

if __name__ == "__main__":
    main()