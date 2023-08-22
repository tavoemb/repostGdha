from backend.entidades import Aplicacion, Empresa
from backend.ip import ObtenerIP, ObtenerIP64
from backend.basic import GetExcept
from Crypto.Cipher import AES
from random import choice


appConfig: Aplicacion = None
iv = bytes([69, 108, 51, 118, 51, 110, 95, 98, 51, 99, 107, 51, 110, 68, 95, 49])
dictKeys = {
    Empresa.Elevenminds: bytes([
        69, 76, 69, 86, 69, 78, 77, 73, 78, 68, 83, 95, 76, 65, 66, 83, 95, 83, 95, 68, 69, 95, 82, 46, 76, 95, 68, 69, 95, 67, 46, 86
    ]),
    Empresa.GlobalTrack: bytes([
        97, 31, 131, 162, 189, 160, 135, 45, 184, 158, 21, 53, 59, 194, 174, 95, 205, 115, 78, 190, 6, 106, 185, 213, 244, 222, 193, 87, 131, 225, 240, 126
    ]),
    Empresa.Innovalinks: bytes([
        139, 28, 176, 194, 147, 114, 198, 106, 230, 189, 57, 184, 49, 67, 33, 236, 32, 96, 155, 215, 178, 55, 251, 68, 44, 47, 85, 144, 188, 170, 234, 204
    ]),
    Empresa.SisTechnologies: bytes([
        32, 223, 149, 23, 229, 200, 115, 180, 14, 11, 244, 212, 109, 8, 243, 61, 1, 199, 53, 91, 161, 101, 102, 80, 168, 148, 159, 115, 145, 197, 251, 244
    ]),
    Empresa.TheRightConnectionsDeMexico: bytes([
        225, 146, 56, 81, 188, 193, 5, 142, 38, 120, 21, 137, 55, 12, 106, 38, 49, 70, 224, 255, 147, 150, 21, 72, 3, 246, 41, 98, 65, 54, 35, 234
    ])
}

def StartSecurity(_AppConfig: Aplicacion) -> bool:
    """
        Inicializa la variable global de configuracion.
    """
    global appConfig
    try:
        appConfig = _AppConfig
        return True
    except:
        return False


def pad(s: str):
    sr = s.encode('utf-8')
    r = (16 - len(sr) % 16) * chr(16 - len(sr) % 16)
    return s + r


def unpad(_String: str):
    if not _String.decode('utf-8').isprintable():
        _String = _String[:-ord(_String[len(_String)-1:])]
    return _String.decode('utf-8')


def Encrypt(_Texto: str) -> str:
    """
        Ecripta un texto mediante algoritmos AES.
    """
    try:
        raw = str(_Texto).encode('utf-8')
        if len(raw) % 16 > 0:
            raw = pad(raw.decode('utf-8')).encode('utf-8')
        cipher = AES.new(dictKeys[appConfig.Empresa], AES.MODE_CBC, iv)
        code = ''
        encoder = cipher.encrypt(raw)
        encoder = encoder.hex()
        for x, y in enumerate(str(encoder).upper()):
            if x % 2 or x == 0:
                code += y
            else:
                code += '-' + y
        return code
    except:
        GetExcept()
        return ''


def Decrypt(_Texto: str) -> str:
    """
        Desencripta un texto codificado con algoritmos AES.
    """
    try:
        enc = _Texto.replace('-', '').upper()
        enc = bytes.fromhex(enc)
        cipher = AES.new(dictKeys[appConfig.Empresa], AES.MODE_CBC, iv)
        return str(unpad(cipher.decrypt(enc)))
    except:
        GetExcept()
        return ''


def GenerarToken(_IdUsuario: int) -> str:
    """
        Genera un token apartir de un id de usuario.
    """
    try:
        ipXUsuario = abs(_IdUsuario) * 5
        if ipXUsuario > 9223372036854775807:
            return ''
        ipAdressUsuario = ObtenerIP(ipXUsuario)
        ips = ipAdressUsuario.split('.')
        posicion = choice([0, 1, 2, 3])
        ips[posicion] = '{}.{}'.format(ips[posicion], abs(_IdUsuario))
        return Encrypt('{}.{}'.format(posicion + 1, '.'.join(ips)))
    except:
        GetExcept()
        return ''


def ValidarToken(_Token: str, _Idusuario: int) -> bool:
    """
        Valida si el token esta conformado correctamente.
    """
    try:
        stringToken = Decrypt(_Token)
        splitToke = stringToken.split('.')
        posicion = int(splitToke[0])
        if int(splitToke[posicion + 1]) == abs(_Idusuario):
            splitToke.pop(posicion + 1)
            splitToke.pop(0)
            ip = '.'.join(splitToke)
            ipXx = ObtenerIP64(ip)
            ipXUsuario = abs(_Idusuario) * 5
            IPFijo = ObtenerIP64(ObtenerIP(ipXUsuario))
            if ipXx == ip or ipXx == IPFijo:
                return True
        return False
    except:
        GetExcept()
        return False
