from psycopg2.pool import PoolError, ThreadedConnectionPool
from backend.entidades import Evento, Metodo, Dominio
from backend.logger import GetExcept, LogErrores
from backend.configuracion import appConfig
from psycopg2.extras import RealDictCursor
from backend.archivo import LogSql
from datetime import datetime
from sqlite3 import connect
from os.path import exists


contadorErroresEnGrupo, limiteErroresEnGrupo = 0, 3
dictGrupoDeConexiones, dictVariablesDeLog = {}, {'Iniciado': False, 'TipoDominio': 0, 'Ambiente': ''}
archivoDeBD = ''
tabla = ''


def EscribirLogSql(_NombreSql: str, _Nota: str, _Consulta: str) -> str:
    """
        crear la estructura principal del log sql.
    """
    global dictVariablesDeLog
    url = ''
    try:
        if not dictVariablesDeLog['Iniciado']:
            dictVariablesDeLog['TipoDominio'] = Dominio.backendCloud.value if appConfig.DominioCloud else Dominio.backend.value
            dictVariablesDeLog['Ambiente'] = appConfig.Ambiente.name.lower() if appConfig.Ambiente.value > 0 else '{}/{}'.format(appConfig.Empresa.name.lower(), appConfig.Ambiente.name.lower())
            dictVariablesDeLog['Iniciado'] = True
        url = LogSql(dictVariablesDeLog['TipoDominio'], appConfig.Dominio, dictVariablesDeLog['Ambiente'], appConfig.IdServicio, appConfig.IdInstalacion, appConfig.NombreServicio, appConfig.IdInicio, appConfig.DirectorioSql, _NombreSql, _Nota, _Consulta)
    except:
        GetExcept()
    finally:
        return url


def IniciarConexion() -> None:
    """
        Inicializa el diccionario de grupo de conexiones para las
        diferentes configuraciones de las base de datos.
    """
    global dictGrupoDeConexiones
    try:
        dictGrupoDeConexiones = {bd: None for bd in appConfig.ServidoresBD.keys()}
        if not exists(archivoDeBD) and archivoDeBD != '':
            EjecutarSqLite(tabla, 'IniciarConexion()')
    except:
        GetExcept()


def ObtenerConexion(_Metodo: Metodo, _Servicio: int, _Funcion: int, _Parte: int) -> list:
    """
        Recibe int tipo de metodo (rest, ws, memoria) y  servicio, funcion, parte que estan en el app.json.
        Retorna el grupo de conexion o None si hubo un error.
    """
    global dictGrupoDeConexiones
    grupoDeConexiones, datos = None, ''
    try:
        funcionBD = 'S{}_F{}_P{}'.format(_Servicio, _Funcion, _Parte)
        if funcionBD in appConfig.FuncionesBD:
            servidorBD = appConfig.FuncionesBD[funcionBD]
            if servidorBD not in dictGrupoDeConexiones or servidorBD not in appConfig.ServidoresBD:
                return
            confguracionBD = appConfig.ServidoresBD[servidorBD]
            if dictGrupoDeConexiones[servidorBD] is None:
                CadenaDeConexion = "application_name='{}' host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(
                    '{}_{}'.format(appConfig.NombreServicio, _Metodo.name)[:64],
                    confguracionBD['Ip'],
                    confguracionBD['Puerto'],
                    confguracionBD['BD'],
                    confguracionBD['Usuario'],
                    confguracionBD['Contrasena']
                )
                dictGrupoDeConexiones[servidorBD] = ThreadedConnectionPool(1, confguracionBD['NumeroConexiones'], CadenaDeConexion)
            grupoDeConexiones = dictGrupoDeConexiones[servidorBD]
            datos = '{}|{}|{}|{}'.format(confguracionBD['Ip'], confguracionBD['Puerto'], confguracionBD['BD'], confguracionBD['Usuario'])
    except:
        GetExcept(Evento.Critico)
        grupoDeConexiones = None
    finally:
        return grupoDeConexiones, datos


def ConsultarSql(_Datos: str, _GrupoDeConexiones: ThreadedConnectionPool, _Consulta: str, _Metodo='') -> list:
    """
        Recibe el grupo de conexiones, el query y opcionalmente le método,
        retorna bool error, int filas afectadas y un arreglo de datos todos
        dentro de una tupla.
    """
    global contadorErroresEnGrupo, limiteErroresEnGrupo
    error, afectados, filas = True, 0, []
    try:
        conexion = _GrupoDeConexiones.getconn()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(_Consulta)
            filas = cursor.fetchall()
            afectados = cursor.rowcount
            error = False
        except Exception as e:
            logSql = EscribirLogSql(_Metodo, '{}|{}\n--{}'.format(datetime.utcnow(), _Datos, str(e).replace('/n', ' ')), _Consulta)
            GetExcept(_Message=_Metodo, _Link=logSql)
        cursor.close()
        conexion.close()
        _GrupoDeConexiones.putconn(conexion)
    except PoolError as pe:
        if str(pe) == 'connection pool exhausted':
            contadorErroresEnGrupo += 1
            if contadorErroresEnGrupo >= limiteErroresEnGrupo:
                IniciarConexion()
        logSql = EscribirLogSql(_Metodo, '{}|{}\n--{}'.format(datetime.utcnow(), _Datos, str(pe).replace('/n', ' ')), _Consulta)
        GetExcept(_Message=_Metodo, _Link=logSql)
    except Exception as e:
        logSql = EscribirLogSql(_Metodo, '{}|{}\n--{}'.format(datetime.utcnow(), _Datos, str(e).replace('/n', ' ')), _Consulta)
        GetExcept(_Message=_Metodo, _Link=logSql)
    finally:
        return error, afectados, filas


def EjecutarSql(_Datos: str, _GrupoDeConexiones: ThreadedConnectionPool, _Consulta: str, _Metodo='') -> list:
    """
        Recibe el grupo de conexiones, el query y opcionalmente le método.
        Retorna bool error e int filas afectadas dentro de una tupla.
    """
    global contadorErroresEnGrupo, limiteErroresEnGrupo
    error, afectados = True, 0
    try:
        connection = _GrupoDeConexiones.getconn()
        cursor = connection.cursor()
        try:
            cursor.execute(_Consulta)
            afectados = cursor.rowcount
            connection.commit()
            error = False
        except Exception as e:
            connection.rollback()
            logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(e).replace('/n', ' ')), _Consulta)
            GetExcept(_Message=_Metodo, _Link=logSql)
        cursor.close()
        _GrupoDeConexiones.putconn(connection)
    except PoolError as pe:
        if str(pe) == 'connection pool exhausted':
            contadorErroresEnGrupo += 1
            if contadorErroresEnGrupo >= limiteErroresEnGrupo:
                IniciarConexion()
        logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(pe).replace('/n', ' ')), _Consulta)
        GetExcept(_Message=_Metodo, _Link=logSql)
    except Exception as e:
        logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(e).replace('/n', ' ')), _Consulta)
        GetExcept(_Message=_Metodo, _Link=logSql)
    finally:
        return error, afectados


def EjecutarConsultaSql(_Datos: str,  _GrupoDeConexiones: ThreadedConnectionPool, _Consulta: str, _Metodo='') -> list:
    """
        Recibe el grupo de conexiones, el query y opcionalmente le método,
        retorna bool error, int filas afectadas y un arreglo de datos todos
        dentro de una tupla.
    """
    global contadorErroresEnGrupo, limiteErroresEnGrupo
    error, afectados, filas = True, 0, []
    try:
        conexion = _GrupoDeConexiones.getconn()
        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(_Consulta)
            filas = cursor.fetchall()
            afectados = cursor.rowcount
            conexion.commit()
            error = False
        except Exception as e:
            conexion.rollback()
            logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(e).replace('/n', ' ')), _Consulta)
            GetExcept(_Message=_Metodo, _Link=logSql)
        cursor.close()
        conexion.close()
        _GrupoDeConexiones.putconn(conexion)
    except PoolError as pe:
        if str(pe) == 'connection pool exhausted':
            contadorErroresEnGrupo += 1
            if contadorErroresEnGrupo >= limiteErroresEnGrupo:
                IniciarConexion()
        logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(pe).replace('/n', ' ')), _Consulta)
        GetExcept(_Message=_Metodo, _Link=logSql)
    except Exception as e:
        logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(e).replace('/n', ' ')), _Consulta)
        GetExcept(_Message=_Metodo, _Link=logSql)
    finally:
        return error, afectados, filas


def TransaccionSql(_Datos: str, _GrupoDeConexiones: ThreadedConnectionPool, _Consultas: tuple, _Metodo='') -> bool:
    """
        Ejecuta varias instrucciones sql y solo si todas se llevan
        a cabo sin ningun problema se realiza un commit y retorna
        un true en caso contrario se realiza un rollback y retorna
        un false.
    """
    global contadorErroresEnGrupo, limiteErroresEnGrupo
    error, bandera = True, False
    try:
        conexion = _GrupoDeConexiones.getconn()
        cursor = conexion.cursor()
        try:
            for query in _Consultas:
                cursor.execute(query)
                if cursor.rowcount < 0:
                    bandera = True
                    break
            if bandera:
                conexion.rollback()
            else:
                conexion.commit()
                error = False
        except Exception as e:
            conexion.rollback()
            for query in _Consultas:
                LogErrores('connection', 'TransactionSql', datetime.utcnow(), _Metodo, str(e), _Consulta=query)
            logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(e).replace('/n', ' ')), '--:SQL:'.join(_Consultas))
            GetExcept(_Message=_Metodo, _Link=logSql)
        cursor.close()
        _GrupoDeConexiones.putconn(conexion)
    except PoolError as pe:
        if str(pe) == 'connection pool exhausted':
            contadorErroresEnGrupo += 1
            if contadorErroresEnGrupo >= limiteErroresEnGrupo:
                IniciarConexion()
        logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(pe).replace('/n', ' ')), '--:SQL:'.join(_Consultas))
        GetExcept(_Message=_Metodo, _Link=logSql)
    except Exception as e:
        logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), _Datos, str(e).replace('/n', ' ')), '--:SQL:'.join(_Consultas))
        GetExcept(_Message=_Metodo, _Link=logSql)
    finally:
        return error


def ConsultarSqLite(_Consulta: str, _Metodo: str) -> tuple:
    """
        Ejecuta una instruccionde consulta para sqlite
        retorna una tupla de los resultados.
    """
    filas = []
    try:
        conexion = connect(archivoDeBD)
        cursor = conexion.cursor()
        try:
            cursor.execute(_Consulta)
            filas = cursor.fetchall()
        except:
            GetExcept(_Message=_Metodo)
        cursor.close()
        conexion.close()
    except:
        GetExcept(_Message=_Metodo)
    return tuple(filas)


def EjecutarSqLite(_Consulta: str, _Metodo: str) -> int:
    """
        Ejecuta una instruccion de sqlite y retorna
        un int de afectados.
    """
    afectados = 0
    try:
        conexion = connect(archivoDeBD)
        cursor = conexion.cursor()
        try:
            cursor.execute(_Consulta)
            afectados = cursor.rowcount
            conexion.commit()
        except:
            conexion.rollback()
            GetExcept(_Message=_Metodo)
        cursor.close()
        conexion.close()
    except:
        GetExcept(_Message=_Metodo)
    finally:
        return afectados
