import hashlib

def build(value: str):
    tmp = hashlib.md5(value.encode())
    return str(tmp.hexdigest())
