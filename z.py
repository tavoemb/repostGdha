from datetime import datetime, timedelta
from backend.ip import ObtenerIP, ObtenerIP64
from random import choice
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto import Random
from datetime import datetime

Registro = "2023-07-04 15:30"

dt_registro = datetime.strptime(Registro, "%Y-%m-%d %H:%M")

dt_nueva_fecha = dt_registro + timedelta(seconds=0)

str_nueva_fecha = dt_nueva_fecha.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

print(str_nueva_fecha)


key = bytes([209, 71, 153, 210, 175, 92, 72, 156, 27, 152, 200, 233, 70, 132, 171, 228, 29, 31, 2, 94, 254, 98, 12, 71, 142, 180, 153, 234, 190, 154, 142, 59])
iv = bytes([178, 132, 23, 251, 142, 201, 254, 86, 42, 123, 29, 68, 69, 79, 122, 255])


def pad(s: str):
    sr = s.encode('utf-8')
    r = (16 - len(sr) % 16) * chr(16 - len(sr) % 16)
    return s + r


def unpad(s: str):
    sr = s[:-ord(s[len(s)-1:])]
    return sr.decode('utf-8')

def Encrypt(_Texto: str) -> str:
    """
        Ecripta un texto mediante algoritmos AES.
    """
    try:
        raw = str(_Texto).encode('utf-8')
        if len(raw) % 16 > 0:
            raw = pad(raw.decode('utf-8')).encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encoder = cipher.encrypt(str(_Texto).encode('utf-8'))
        return encoder
    except Exception as Ex:
        #GetExcept()
        return ''


def Decrypt(_Texto: str) -> str:
    """
        Desencripta un texto codificado con algoritmos AES.
    """
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return str(unpad(cipher.decrypt(_Texto)))
    except:
        #GetExcept()
        return ''
    

txt= "hola mundo"
txt = Encrypt(txt)
print(txt)

print("Mebnsaje: ", Decrypt(txt))

