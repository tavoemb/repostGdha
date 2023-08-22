from backend.ip import ObtenerIP, ObtenerIP64
from random import choice
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto import Random


keyPsw = b'5029BBCA6A8EFB18DEC2A28517B044D8'
BS = len(keyPsw)
padPsw = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpadPsw = lambda s : s[:-ord(s[len(s)-1:])]


#region "---+ Encriptar y Desencriptar PSW  +---"

def encryptPsw(raw):
    try:
        raw = padPsw(str(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(keyPsw, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw.encode('utf8')))
    except Exception as e:
        print('Error: {}'.format(e))


def DecryptPsw(_Texto: str):
    try:
        enc = b64decode(_Texto)
        iv = enc[:16]
        cipher = AES.new(keyPsw, AES.MODE_CBC, iv)
        return str(unpadPsw(cipher.decrypt(enc[16:])))[2:-1]
    except Exception as e:
        print('Error: {}'.format(e))

#endregion

