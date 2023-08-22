from backend.basic import GetExcept
from time import mktime, tzname
from datetime import datetime
from dateutil import tz


def CentroToUtc(_Date: datetime) -> datetime or None:
    """
        Retorna la fecha Mexico/General en horario UTC.
        Si falla retorna None.
    """
    try:
        centro = _Date.replace(tzinfo=tz.gettz('Mexico/General'))
        utca = centro.astimezone(tz.tzutc())
        utca = utca.replace(tzinfo=None)
        return utca
    except:
        GetExcept()
        return None


def datetime_IdUnix(_IdUnix: float) -> datetime or None:
    """
        Retorna un objeto datetime equivalente al numero flotante
        idUnix que recive, si falla retorna la fecha 2000-01-01.
    """
    try:
        return datetime.fromtimestamp(_IdUnix)
    except:
        return None


def datetime_IsoWeb(_Date: str) -> datetime or None:
    """
        Retorna un tipo fecha de una cadena con formato 2020-01-01T00:00:00.000Z
        Si falla retorna None.
    """
    try:
        return datetime.strptime(_Date, '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        return None


def datetime_Fecha(_Date: str) -> datetime or None:
    """
        Retorna un tipo fecha de una cadena con formato 2020-01-01
        Si falla retorna None.
    """
    try:
        return datetime.strptime(_Date, '%Y-%m-%d')
    except:
        GetExcept()
        return None


def datetime_FechaHora(_Date: str) -> datetime or None:
    """
        Retorna un tipo fecha de una cadena con formato 2020-01-01 00:00:00.000
        Si falla retorna None.
    """
    try:
        return datetime.strptime(_Date, '%Y-%m-%d %H:%M:%S.%f')
    except:
        GetExcept()
        return None


def datetime_str(_Date: str, _Format: str) -> (datetime or None):
    """
        Convierte un string a tipo fecha, en el caso de un error retornara un valor nulo.
    """
    try:
        return datetime.strptime(_Date, _Format)
    except:
        GetExcept()
        return None


def IdUnix() -> float:
    """
        Retorna un numero flotante desde la fecha utc actual
        por lo tanto es unico e irrepetible, si falla retorna
        el valor basico 946706400.0 equivalente a la fecha
        2000-01-01.
    """
    try:
        dt = datetime.utcnow()
        microsec = float('0.{}'.format(dt.microsecond))
        unix = mktime(dt.timetuple()) + microsec
        return unix
    except:
        return 946706400.0


def MonthOfYear(_Datetime: datetime) -> str:
    """
        Retorna un numero str en convinacion del año y el numero del mes.
    """
    try:
        return '{}{}'.format(_Datetime.year, str(_Datetime.month).zfill(2))
    except:
        GetExcept()
        return ''


def MonthOfYear_datetime(_MonthOfYear: str) -> str:
    """
    """
    try:
        return datetime(int(_MonthOfYear[:4]), int(_MonthOfYear[4:]), 1) if len(_MonthOfYear) == 6 else None
    except:
        GetExcept()
        return None


def NoroesteToUtc(_Date: datetime) -> datetime or None:
    """
        Retorna la fecha Mexico/BajaNorte en horario UTC.
        Si falla retorna None.
    """
    try:
        centro = _Date.replace(tzinfo=tz.gettz('Mexico/BajaNorte'))
        utca = centro.astimezone(tz.tzutc())
        utca = utca.replace(tzinfo=None)
        return utca
    except:
        GetExcept()
        return None


def PacificoToUtc(_Date: datetime) -> datetime or None:
    """
        Retorna la fecha Mexico/BajaSur en horario UTC.
        Si falla retorna None.
    """
    try:
        centro = _Date.replace(tzinfo=tz.gettz('Mexico/BajaSur'))
        utca = centro.astimezone(tz.tzutc())
        utca = utca.replace(tzinfo=None)
        return utca
    except:
        GetExcept()
        return None


def SecondsToHours(_Seconds: int) -> float:
    """
        Convierte un objeto de tipo timedelta en representacion de
        float el cual hace referencia a las horas como un entero y
        los decimales representan los minutos en porcentaje. Por
        ejemplo 1:30 hrs es igual a 1.5 en representacion flotante.
    """
    try:
        totalSeconds = _Seconds
        totalHours = round((totalSeconds // 60) // 60)
        totalMinutes = round((1 / 60) * ((totalSeconds - (totalHours * 3600)) // 60), 2)
        return totalHours + totalMinutes
    except:
        GetExcept()
        return 0.0


def str_Fecha(_Date: datetime) -> str or None:
    """
        Retorna el formato 2000-01-01
        Si falla retorna None.
    """
    try:
        return _Date.strftime('%Y%m%d')
    except:
        GetExcept()
        return None


def str_FechaCorta(_Date: datetime, _WithTime=False) -> str or None:
    """
        Retorna el formato 20200101.
        Si falla retorna None.
    """
    resultado = None
    try:
        resultado = _Date.strftime('%Y%m%d%H%M%S') if _WithTime else _Date.strftime('%Y%m%d')
    except:
        GetExcept()
    finally:
        return resultado


def str_FechaHora(_Date: datetime, _Hrs=24) -> str or None:
    """
        Retorna el formato 2020-01-01 00:00:00.000
        o 2020-01-01 00:00:00 AM, Si falla retorna None.
    """
    try:
        if _Hrs == 24:
            return _Date.strftime('%Y-%m-%d %H:%M:%S.%f')[:23]
        return _Date.strftime('%Y-%m-%d %I:%M:%S %p')[:23]
    except:
        GetExcept()
        return None


def str_datetime(_Date: datetime, _Format: str) -> str or None:
    """
        Retorna el formato especificado de un datetime, Si falla retorna None.
    """
    try:
        return _Date.strftime(_Format)
    except:
        GetExcept()
        return None


def str_IsoWeb(_Date: datetime) -> str or None:
    """
        Retorna el formato 2020-01-01T00:00:00.000Z
        Si falla retorna None.
    """
    try:
        return '{}Z'.format(_Date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:23])
    except:
        return None


def UtcToCentro(_Date: datetime) -> datetime or None:
    """
        Retorna la fecha UTC en horario Mexico/General.
        Si falla retorna None.
    """
    try:
        utc = _Date.replace(tzinfo=tz.gettz('UTC'))
        central = utc.astimezone(tz.gettz('Mexico/General'))
        central = central.replace(tzinfo=None)
        return central
    except:
        GetExcept()
        return None


def UtcToNoroeste(_Date: datetime) -> datetime or None:
    """
        Retorna la fecha UTC en horario Mexico/BajaNorte.
        Si falla retorna None.
    """
    try:
        utc = _Date.replace(tzinfo=tz.gettz('UTC'))
        central = utc.astimezone(tz.gettz('Mexico/BajaNorte'))
        central = central.replace(tzinfo=None)
        return central
    except:
        GetExcept()
        return None


def UtcToPacifico(_Date: datetime) -> datetime or None:
    """
        Retorna la fecha UTC en horario Mexico/BajaSur.
        Si falla retorna None.
    """
    try:
        utc = _Date.replace(tzinfo=tz.gettz('UTC'))
        central = utc.astimezone(tz.gettz('Mexico/BajaSur'))
        central = central.replace(tzinfo=None)
        return central
    except:
        GetExcept()
        return None


def WeekOfYear(_Datetime: datetime) -> str:
    """
        Retorna un numero str en convinacion del año y el numero de la semana.
    """
    try:
        day = int(_Datetime.strftime('%j'))
        tmp = day // 7
        tmp = 1 if tmp == 0 else tmp
        tmp = tmp + 1 if day > (tmp * 7) else tmp
        return '{}{}'.format(_Datetime.strftime('%Y'), str(tmp).zfill(2))
    except:
        GetExcept()
        return ''


def ZoneToUtc(_Date: datetime, _Zone: tzname) -> datetime or None:
    """
        Retorna la fecha Mexico/General en horario UTC.
        Si falla retorna None.
    """
    try:
        zona = _Date.replace(tzinfo=tz.gettz('{}'.format(tzname[0])))
        utca = zona.astimezone(tz.tzutc())
        utca = utca.replace(tzinfo=None)
        return utca
    except:
        return None
