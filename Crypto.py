import os
import json
import binascii

try:
    open('keys/data.json', 'x').close()
except FileExistsError:
    pass

def rsa_keygen() -> bool:
    os.system('openssl genpkey -algorithm RSA -out keys/secret.pem')
    os.system('openssl rsa -in keys/secret.pem -pubout -out keys/public.pem')
    return True

def rsa_sign(data: str) -> str:
    with open('keys/data.json', 'w') as f:
        json.dump(data, f)
    os.system('openssl dgst -sha256 -binary -sign keys/secret.pem -out keys/sig.bin keys/data.json')
    sig = open('keys/sig.bin', 'rb').read()
    return sig.hex()

def rsa_verify(transaction: dict) -> bool:
    b = binascii.unhexlify(transaction['signature'])
    pk = transaction['public_key']
    open('keys/pk.pem', 'w').write(pk)
    open('keys/sig.bin', 'wb').write(b)
    v = os.system('openssl dgst -sha256 -binary -verify keys/public.pem -signature keys/sig.bin keys/data.json')
    if v == 'Verification OK' or v == '0' or v == 0:
        return True
    return False
