from backend.fecha import str_IsoWeb
from backend.basic import GetExcept
from bitarray import bitarray, util
from datetime import datetime


dictTypes = {'bol': False, 'flt': 0.0, 'geo': (0.0, 0.0), 'int': 0, 'str': '', 'list': [], 'jsn': {}}
dictQuote = {'bol': False, 'dt': 'Null', 'flt': 0.0, 'geo': 'ST_GeomFromWKB(null,4326)', 'int': 0, 'str': ''}
dictType2 = {'bol': False, 'dt': None, 'flt': 0.0, 'geo': None, 'int': 0, 'str': '', 'list': [], 'jsn': {}}
dictTypesValidarParametros = {'bol': False, 'dt': None, 'flt': 0.0, 'int': 0, 'str': '', 'list<int>': [], 'list<str>': []}
SYMBOLS = {
    'personalized': ('Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'),
    'customary': ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
    'customary_ext': ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa', 'zetta', 'iotta'),
    'iec': ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
    'iec_ext': ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi', 'zebi', 'yobi'),
}


def FormatNotNone(_Type: str, _Object: object) -> object:
    """
        Devuelve el valor base para cada tipo.
    """
    try:
        if _Type == 'dt':
            _Type, _Object = 'str', str_IsoWeb(_Object)
        if _Type == 'geo':
            geo = _Object.toJson()
        return dictTypes[_Type] if _Object is None else _Object
    except:
        GetExcept()
        return None


def FormatNotNull(_Type: str, _Object: object) -> object:
    """
        Devuelve el valor base para cada tipo.
    """
    try:
        return dictType2[_Type] if _Object is None else _Object
    except:
        GetExcept()
        return None


def QuoteLiteral(_Type: str, _Object: object) -> object:
    """
        Null o la fecha en formato para insertar en sql
    """
    try:
        return dictQuote[_Type] if _Object is None else "'{}'".format(_Object) if _Type == 'dt' else _Object
    except:
        GetExcept()
        return 'Null'


def QuoteNullable(_Object: object) -> object:
    """
        Null o la fecha en formato para insertar en sql
    """
    try:
        return 'Null' if _Object is None else _Object
    except:
        GetExcept()
        return 'Null'


def IntToBit(value: int) -> tuple:
    """
        Convierte un numero entero a un arreglo de bits.
    """
    try:
        resultado = [int(x) for x in '{0:b}'.format(value)[::-1]]
        return tuple(resultado) if len(resultado) > 1 else (0, 0)
    except:
        return (0, 0)


def bytes2human(_Bytes: int, _Symbols='personalized') -> str:
    """
        Retorna un string con la representacion de la cantidad.
    """
    try:
        if _Bytes < 0:
            raise ValueError('The value of _Bytes is less than 0.')
        prefix, symbols = {}, SYMBOLS[_Symbols]
        for index, symbol in enumerate(symbols[1:]):
            prefix[symbol] = 1 << (index + 1) * 10
        for symbol in reversed(symbols[1:]):
            if _Bytes >= prefix[symbol]:
                value = float(_Bytes) / prefix[symbol]
                return '{} {}'.format(round(value, 2), symbol)
        return '{} {}'.format(_Bytes, symbols[0])
    except:
        return '0.0 {}'.format(SYMBOLS[_Symbols][0])


def human2bytes(_String: str, _Symbols='personalized') -> int:
    """
        Retorna un numero int con la cantidad de bytes en el string.
    """
    resultado = 0
    try:
        num = ''
        while _String and (_String[0:1].isdigit() or _String[0:1] == '.'):
            num += _String[0]
            _String = _String[1:]
        letter, num, prefix = _String.strip(), float(num), {SYMBOLS[_Symbols][0]: 1}
        for index, symbol in enumerate(SYMBOLS[_Symbols][1:]):
            prefix[symbol] = 1 << (index + 1) * 10
        resultado = int(num * prefix[letter])
    except Exception as e:
        print(e)
    finally:
        return resultado


def BitArray(_Byte: bytes, length: int) -> list:
    """
        Retorna una lista de bits de los bytes y
        la longitud recivida.
    """
    bitArray = []
    try:
        string = '{0:b}'.format(_Byte)
        bitArray = [bool(int(bit)) for bit in reversed(string)]
        bitArray += [False for i in range(length - len(string))]
    except:
        GetExcept()
    return bitArray


def ProcesarBanderas(_Bandera: int) -> list:
    """
        Recive el numero de la bandera para convertirlo a
        entradas y porcentaje de la bateria, retorna un
        str e int.
    """
    entradas, porcentaje = '', 0.0
    try:
        bytesBandera = _Bandera.to_bytes(8, 'little')
        bytesEntrada = BitArray(bytesBandera[0], 8)
        if bytesEntrada[0]:
            for i in range(1, 7):
                entradas += '{}'.format(int(bytesEntrada[i]))
        else:
            entradas = '000000'
        baBateria = BitArray(bytesBandera[2], 8)
        baPorcentaje = BitArray(0, 16)
        if baBateria[0]:
            baPorcentaje[0] = baBateria[0]
        if baBateria[1]:
            baPorcentaje[1] = baBateria[1]
        if baBateria[2]:
            baPorcentaje[2] = baBateria[2]
        if baBateria[3]:
            baPorcentaje[3] = baBateria[3]
        tbyteInfo = bitarray(baPorcentaje, 'little')
        tbyteInfo = util.ba2int(tbyteInfo)
        porcentaje = round(tbyteInfo * 6.67)
    except:
        GetExcept()
    finally:
        return entradas, porcentaje


def ProcesarIntDatos(_Bandera: int) -> list:
    """
        Recive el numero de int_datos para convertirlo a
        humedad, temperatura y estado de puerta.
    """
    humedad, puerta, temperatura = 0.0, False, 0.0
    try:
        bytesBandera = _Bandera.to_bytes(8, 'little')
        try:
            temperatura = round(int.from_bytes(bytesBandera[1:3], 'little') * 0.01, 2)
        except:
            pass
        try:
            humedad = round(int.from_bytes(bytesBandera[3:5], 'little') * 0.01, 2)
        except:
            pass
        try:
            puerta = True if bytesBandera[5] else False
        except:
            pass
    except:
        GetExcept()
    finally:
        return humedad, puerta, temperatura


def ToInt32(number: int):
    number = round(number)
    if -2147483648 <= number <= 2147483647:
        return number
    else:
        raise NotImplementedError("<class 'ToInt32'> The number is out of range")


def ValidarParametros(_DictParameters: list, _Dictvalues: dict) -> list:
    datos, mensaje, resultado = {}, '', -10001
    try:
        for parameter, attributes in _DictParameters.items():
            if parameter in _Dictvalues:
                try:
                    if attributes['type'] == 'bol':
                        if isinstance(_Dictvalues[parameter], bool):
                            datos[parameter] = bool(_Dictvalues[parameter])
                        else:
                            raise Exception('invalid literal for bool()')
                    if attributes['type'] == 'dt':
                        if isinstance(_Dictvalues[parameter], str):
                            datos[parameter] = datetime.strptime(_Dictvalues[parameter], '%Y-%m-%dT%H:%M:%S.%fZ')
                        elif _Dictvalues[parameter] is None:
                            datos[parameter] = None
                        else:
                            raise Exception('invalid literal for dt()')
                    if attributes['type'] == 'flt':
                        if isinstance(_Dictvalues[parameter], float):
                            datos[parameter] = float(_Dictvalues[parameter])
                        else:
                            raise Exception('invalid literal for float()')
                    if attributes['type'] == 'int':
                        if isinstance(_Dictvalues[parameter], int):
                            datos[parameter] = int(_Dictvalues[parameter])
                        else:
                            raise Exception('invalid literal for int()')
                    if attributes['type'] == 'str':
                        if isinstance(_Dictvalues[parameter], str):
                            datos[parameter] = str(_Dictvalues[parameter])
                        else:
                            raise Exception('invalid literal for str()')
                    if attributes['type'] == 'list<int>':
                        if isinstance(_Dictvalues[parameter], list):
                            listData = []
                            for x in list(_Dictvalues[parameter]):
                                try:
                                    listData.append(int(x))
                                except:
                                    raise Exception('invalid literal for list<int>')
                            if attributes['required'] and len(listData) == 0:
                                raise Exception("the '{}' parameter is required".format(parameter))
                            datos[parameter] = listData
                        else:
                            raise Exception('invalid literal for list<int>')
                    if attributes['type'] == 'list<str>':
                        if isinstance(_Dictvalues[parameter], list):
                            listData = []
                            for x in list(_Dictvalues[parameter]):
                                try:
                                    listData.append(str(x))
                                except:
                                    raise Exception('invalid literal for list<str>')
                            if attributes['required'] and len(listData) == 0:
                                raise Exception("the '{}' parameter is required".format(parameter))
                            datos[parameter] = listData
                        else:
                            raise Exception('invalid literal for list<str>')
                except Exception as e:
                    mensaje += "El parametro '{}' no cumple con el tipo '{}' ({}). ".format(parameter, attributes['type'], e)
            else:
                if attributes['required']:
                    mensaje += "El parametro '{}' es obligatorio. ".format(parameter)
                else:
                    datos[parameter] = dictTypes[attributes['type']]
        if mensaje == '':
            resultado = 1
            mensaje = 'Ok'
    except:
        GetExcept()
        resultado = -10001
    finally:
        return datos, mensaje, resultado
