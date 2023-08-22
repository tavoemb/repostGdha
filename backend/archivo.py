from backend.fecha import str_Fecha, str_FechaCorta, str_FechaHora, UtcToCentro
from datetime import datetime, timedelta
from backend.basic import GetExcept
from os.path import exists
from os import makedirs
from os import path


def CrearDirectorio(_Directorio:str) -> None:
    """
        Se crea el directorio si no existe.
    """
    try:
        if not exists(_Directorio):
            makedirs(_Directorio)
    except:
        GetExcept()


def ExisteArchivo(_Directorio:str) -> bool:
    """
        Valida si un directorio existe.
    """
    try:
        return exists(_Directorio)
    except:
        GetExcept()
        return False


def ObtenerDirectorio(_Directorios:list) -> str or None:
    """
        Obtiene el directorio actual.
    """
    try:
        fecha = str_Fecha(datetime.utcnow())
        DirectorioDia = '{}/{}/{}'.format(1, 2, fecha)
        CrearDirectorio(DirectorioDia)
        if len(_Directorios > 0):
            for directorio in _Directorios:
                if directorio != '':
                    DirectorioDia = '{}/{}'.format(DirectorioDia, directorio)
                    CrearDirectorio(DirectorioDia)
        del fecha
        return DirectorioDia
    except:
        GetExcept()
        return None


def LogAlerta(_IdInicio: int, _DirectorioAlerta: str, _DirectorioLog: str, _NombreAlerta: str, _ListEncabezados: list, _ListValores: list):
    """
        Escribe el log de la alerta que se envio'
    """
    try:
        datetimeUtc = datetime.utcnow()
        pathFile = '{}/{}_{}_Alerta{}.csv'.format(_DirectorioAlerta, _IdInicio, str_FechaCorta(datetimeUtc, True), _NombreAlerta)
        with open('{}/Inicio.csv'.format(_DirectorioLog), 'a') as file:
            file.write('\n"{}","{}","{}","{}"'.format(_IdInicio, str_FechaHora(datetimeUtc), 'Alerta', pathFile))
        with open(pathFile, 'w') as file:
            file.write('{}'.format(','.join(['"{}"'.format(valor) for valor in _ListEncabezados])))
            file.write('\n{}'.format(','.join(['"{}"'.format(valor) for valor in _ListValores])))
    except:
        GetExcept()


def LogSql(_TipoDominio: int, _Dominio: str, _Ambiente: str, _IdServicio: int, _IdInstacia: int, _NombreServicio, _IdInicio: int, _DirectorioSql: str, _NombreSql: str, _Nota: str, _Query: str) -> str:
    """
        Escribe el log de las consultas erradas.
    """
    pathUrl = ''
    try:
        datetimeUtc = datetime.utcnow()
        fileName = '{}_{}_{}.sql'.format(_IdInicio, str_FechaCorta(datetimeUtc, True), _NombreSql)
        pathFile = '{}/{}'.format(_DirectorioSql, fileName)
        pathUrl = '[LogSql](https://rest{}.{}/sql/{}/{}_{}_{}/{})'.format(_TipoDominio, _Dominio, _Ambiente, _IdServicio, _IdInstacia, _NombreServicio, fileName)
        with open(pathFile, 'w') as file:
            file.write('--{}'.format(_Nota))
            file.write('\n{}'.format(_Query))
    except:
        GetExcept()
    finally:
        return pathUrl


def LogMemoria(_Log: bool, _DirectorioLog: str, _Metodo: str, _Contador: int, _Duracion: timedelta) -> None:
    """
        Escribe el log de la memoria.
    """
    try:
        if _Log:
            datetimeUtc = datetime.utcnow()
            pathFile = '{}/{}_{}_Memoria.csv'.format(_DirectorioLog, str_FechaCorta(datetimeUtc), str(datetimeUtc.hour).zfill(2))
            if not ExisteArchivo(pathFile):
                with open(pathFile, 'w') as file:
                    file.write('"Fecha","Memoria","Registros","Duracion (seg)"')
            with open(pathFile, 'a') as file:
                file.write('\n"{}","{}","{}","{}"'.format(datetimeUtc, _Metodo, _Contador, _Duracion.total_seconds()))
    except:
        GetExcept()


def LogProceso(_DirectorioLog: str, _Duracion: timedelta, _Metodo: str, _Mensaje: str) -> None:
    """
        Escribe el log principal del proceso.
    """
    try:
        datetimeUtc = datetime.utcnow()
        pathFile = '{}/{}_{}_Proceso.csv'.format(_DirectorioLog, str_FechaCorta(datetimeUtc), str(datetimeUtc.hour).zfill(2))
        if not ExisteArchivo(pathFile):
            with open(pathFile, 'w') as file:
                file.write('"Fecha","Proceso","Duracion (seg)","Mensaje"')
        with open(pathFile, 'a') as file:
            file.write('\n"{}","{}","{}","{}"'.format(datetimeUtc, _Metodo, _Duracion.total_seconds(), _Mensaje))
    except:
        GetExcept()


def LogInicio(_InicioDinamico: bool, _DirectorioLog: str, _Empresa: str, _Ambiente: str) -> int:
    """
        Escribe el log principal del inicio.
    """
    resultado = 0
    try:
        pathFile = '{}/Inicio.csv'.format(_DirectorioLog)
        resultado = 1
        if ExisteArchivo(pathFile):
            if _InicioDinamico:
                with open(pathFile, 'r') as file:
                    lineas = file.readlines()
                    resultado = 1 + int(lineas[-1].split(',')[0].replace('"', ''))
        else:
            with open(pathFile, 'w') as file:
                file.write('"Inicio","Fecha","Empresa","Ambiente"')
        with open(pathFile, 'a') as file:
            file.write('\n"{}","{}","{}","{}"'.format(resultado, datetime.utcnow(), _Empresa, _Ambiente))
    except Exception as e:
        print(e)
        resultado = 0
        GetExcept()
    finally:
        return resultado


def CrearArchivoSistema(_Ambiente: str, _IdServicio: int, _IdInstalacion: int, _Servicio: str, _Descripcion: str, _Usuario='rcrescencio', _Python='/usr/bin/python3', _Main='principal.py') -> str:
    """
        _summary_
    """
    nameFile = ''
    try:
        nameFile = '_{}_{}_{}_{}.service'.format(_Ambiente, _IdServicio, _IdInstalacion, _Servicio)
        pathFile = '/etc/systemd/system/{}'.format(nameFile)
        if exists(pathFile):
            nameFile = 'El archivo ya existe: {}'.format(nameFile)
        else:
            rutaEjecutable = '/'.join(path.dirname(path.realpath(__file__)).split('/')[:-1])
            with open(pathFile, 'w') as file:
                batch = '[Unit]\n'
                batch += 'Description=_{} {}\n'.format(_Ambiente, _Descripcion)
                batch += 'After=multi-user.target\n\n'
                batch += '[Install]\n'
                batch += 'WantedBy=multi-user.target\n\n'
                batch += '[Service]\n'
                batch += 'Type=simple\n'
                batch += 'User={}\n'.format(_Usuario)
                batch += 'WorkingDirectory={}\n'.format(rutaEjecutable)
                batch += 'ExecStart={} {}/{}\n'.format(_Python, rutaEjecutable, _Main)
                batch += 'Restart=always'
                file.writelines(batch)
            nameFile = 'El archivo se creo: {}'.format(nameFile)
    except:
        GetExcept()
    return nameFile
