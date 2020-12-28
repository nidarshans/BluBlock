import os
import json
import binascii
os.system('touch data.json')

def keygen() -> bool:
    os.system('openssl genpkey -algorithm RSA -out private.pem')
    os.system('openssl rsa -in private.pem -pubout -out public.pem')
    return True

def sign(data: str) -> str:
    with open('data.json', 'w') as f:
        json.dump(data, f)
    os.system('openssl dgst -sha256 -binary -sign private.pem -out sig.datq data.json')
    sig = open('sig.datq', 'rb').read()
    return sig.hex()

def verify(transaction : dict):
    b = binascii.unhexlify(transaction['signature'])
    open('sig.dat', 'wb').write(b)
    return os.system('openssl dgst -sha256 -binary -verify public.pem -signature sig.dat data.json')
