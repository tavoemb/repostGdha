from backend.configuracion import appConfig
from backend.entidades import Metodo
from backend.logger import GetExcept
from backend.ip import ObtenerIP
from datetime import datetime
from psycopg2 import connect
from socket import AF_INET, SOCK_DGRAM, socket
from threading import Thread


datos = {
    'direccionIp': '192.168.141.16',
    'puerto': 5500,
    'baseDeDatos': 'mit',
    'usuario': 'dev1',
    'contraseña': '4362.n1c0',
}

class RespuestaMas:
    """
        Estructura de un objeto RespuestaMas.
    """
    def __init__(self):
        """
            Inicializa un objeto RespuestaMas.
        """
        self.idMas = 0
        self.nombreMas = ''
        self.puertoEscucha = 0
        self.fechaReporte = datetime(2000, 1, 1)
        self.ipEquipo = 0


class Configuracion:
    """
        Estructura de un objeto Configuracion.
    """
    def __init__(self):
        """
            Inicializa un objeto Configuracion.
        """
        self.int_id = 0
        self.int_ip = ''
        self.var_nombre = ''
        self.int_puerto = 0
        self.int_puerto_envia = 0
        self.bol_enviar_sms = False
        self.int_minutos_alerta = 0
        self.int_minutos_recordatorio = 0
        self.bol_envia_mas = False
        self.var_equipo = ''
        self.var_servicio = ''
        self.bol_enuso = False
        self.dt_modificacion = datetime(2000, 1, 1)
        self.dt_ultimo_reporte = datetime(2000, 1, 1)
        self.int_idmas = 0
        self.var_descripcion = ''


configuracion = Configuracion()
respuesta = RespuestaMas()


def ConsultarSql(_Consulta: str) -> list:
    error, afectados, filas = True, 0, tuple()
    try:
        cadenaDeConexion = "application_name='LoadConfigurationServiceUdp' host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(
            datos['direccionIp'], datos['puerto'], datos['baseDeDatos'], datos['usuario'], datos['contraseña']
        )
        conexion = connect(cadenaDeConexion)
        cursor = conexion.cursor()
        try:
            cursor.execute(_Consulta)
            filas = cursor.fetchall()
            afectados = cursor.rowcount
        except:
            GetExcept(_Method=Metodo.Udp, _Envia=False)
        cursor.close()
        conexion.close()
        filas = tuple(filas)
        error = False
    except:
        GetExcept(_Method=Metodo.Udp, _Envia=False)
    finally:
        return error, afectados, filas


def ObtenerConfiguracion() -> bool:
    global configuracion
    valido = False
    try:
        sql = """
            SELECT
                int_id, int_ip, var_nombre, int_puerto, int_puerto_envia,
                bol_enviar_sms, int_minutos_alerta, int_minutos_recordatorio,
                bol_envia_mas, var_equipo, var_servicio, bol_enuso,
                dt_modificacion, dt_ultimo_reporte, int_idmas, var_descripcion
            FROM tmp.servicio_mas
            WHERE var_nombre='{}' AND LOWER(var_equipo)='{}';
        """.format(appConfig.NombreServicio, appConfig.NombreEquipo.lower())
        error, efactados, filas = ConsultarSql(sql)
        if not error or efactados > 0:
            configuracionMas = Configuracion()
            configuracionMas.int_id = filas[0][0]
            configuracionMas.int_ip = ObtenerIP(filas[0][1])
            configuracionMas.var_nombre = filas[0][2]
            configuracionMas.int_puerto = filas[0][3]
            configuracionMas.int_puerto_envia = filas[0][4]
            configuracionMas.bol_enviar_sms = filas[0][5]
            configuracionMas.int_minutos_alerta = filas[0][6]
            configuracionMas.int_minutos_recordatorio = filas[0][7]
            configuracionMas.bol_envia_mas = filas[0][8]
            configuracionMas.var_equipo = filas[0][9]
            configuracionMas.var_servicio = filas[0][10]
            configuracionMas.bol_enuso = filas[0][11]
            configuracionMas.dt_modificacion = filas[0][12]
            configuracionMas.dt_ultimo_reporte = filas[0][13]
            configuracionMas.int_idmas = filas[0][14]
            configuracionMas.var_descripcion = filas[0][15]
            configuracion = configuracionMas
            valido = True
    except Exception as e:
        GetExcept(_Method=Metodo.Udp, _Send=False)
    finally:
        return valido


def EnviarMensajeUdp() -> None:
    global configuracion, respuesta
    try:
        if respuesta.idMas != 0 and configuracion.int_id != 0:
            mensaje = '{}|{}|{}|{}|{}'.format(
                configuracion.int_id,
                configuracion.var_nombre,
                configuracion.int_puerto,
                datetime.utcnow().strftime('%Y:%m:%d:%H:%M:%S'),
                configuracion.int_ip
            )
            cliente = socket(AF_INET, SOCK_DGRAM)
            cliente.bind((configuracion.int_ip, configuracion.int_puerto_envia))
            cliente.sendto(mensaje.encode('utf-8'), (respuesta.ipEquipo, respuesta.puertoEscucha))
            del cliente
    except:
        GetExcept(_Method=Metodo.Udp)


def IniciarServidorUdp() -> None:
    global configuracion, respuesta
    try:
        if configuracion.int_id != 0:
            with socket(AF_INET, SOCK_DGRAM) as servidor:
                servidor.bind((configuracion.int_ip, configuracion.int_puerto))
                while True:
                    datos, direccion = servidor.recvfrom(1024)
                    try:
                        parametro = datos.decode('utf-8').split('|')
                        fecha = parametro[3].split(':')
                        respuesta.fechaReporte = datetime(
                            int(fecha[0]), int(fecha[1]),
                            int(fecha[2]), int(fecha[3]),
                            int(fecha[4]), int(fecha[5])
                        )
                        respuesta.idMas = int(parametro[0])
                        respuesta.ipEquipo = str(parametro[4])
                        respuesta.nombreMas = str(parametro[1])
                        respuesta.puertoEscucha = int(parametro[2])
                    except:
                        try:
                            servidor.sendto(datos, direccion)
                        except:
                            pass
                        GetExcept(_Method=Metodo.Udp, _Envia=False)
    except:
        GetExcept(_Method=Metodo.Udp, _Envia=False)
    finally:
        IniciarServidorUdp()


def IniciarClienteMAS() -> bool:
    resultado = False
    try:
        cargaConfiguracion = ObtenerConfiguracion()
        if cargaConfiguracion:
            appConfig.UDP['PuertoEscucha'] = configuracion.int_puerto
            appConfig.UDP['PuertoEnvia'] = configuracion.int_puerto_envia
            Thread(None, IniciarServidorUdp, 'ClienteMas').start()
            resultado = True
    except:
        GetExcept(_Method=Metodo.Udp)
    finally:
        return resultado
