from backend.basic import GetExcept
from ipaddress import IPv4Address
from socket import gethostname
import netifaces


def ObtenerIPs() -> list:
    """
        Retorna la direccion ip del equipo 192.168.0.1
    """
    ips = []
    try:
        for interface in netifaces.interfaces():
            inter = netifaces.ifaddresses(interface)
            for value in inter.values():
                if 'addr' in value[0]:
                    ip = str(value[0]['addr'])
                    if '.' in ip and ip != '127.0.0.1':
                        if len(ip.split('.')[0]) < 4:
                            ips.append(value[0]['addr'])
        ips.sort()
    except:
        GetExcept()
    finally:
        return ips


def ObtenerDireccionIP() -> str:
    """
        Retorna la direccion ip del equipo 192.168.0.1
    """
    try:
        return ObtenerIPs()[0]
    except:
        GetExcept()
        return ''


def ObtenerIP64(_Ip: str) -> int:
    """
        Retorna el valor de la ip en un int64
    """
    try:
        return int(IPv4Address('.'.join(_Ip.split('.')[::-1])))
    except:
        GetExcept()
        return 0


def ObtenerIP(_Ip: int) -> str:
    """
        Retorna el valor de la ip en formato 192.168.0.1
    """
    try:
        return '.'.join(str(IPv4Address(_Ip)).split('.')[::-1])
    except:
        GetExcept()
        return '0.0.0.0'
