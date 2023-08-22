from backend.ip import ObtenerDireccionIP, ObtenerIP, ObtenerIP64, gethostname, ObtenerIPs
from backend.entidades import Ambiente, Aplicacion, Empresa, Evento, Servicio
from backend.archivo import CrearDirectorio, LogInicio
from backend.seguridad import Decrypt, StartSecurity
from backend.fecha import str_FechaHora
from backend.basic import GetExcept
from colorama import Fore, Style
from datetime import datetime
from json import load
import locale


URLELEVENMINDS = 'http://elevenminds.com'
LOGOELEVENMINDS = 'images/logo_elevenminds.png'
PROYECTO = 'Elevenminds'

appConfig = Aplicacion()
DicPropiedades = {}


def ConfiguracionAmbiente() -> bool:
    """
        Configura las variables de acuerdo al ambiente.
    """
    global appConfig
    resultado = False
    try:
        appConfig.NombreCorreo = '{} {}'.format(appConfig.Ambiente.name, appConfig.NombreServicio)
        appConfig.DestinatariosUrgentes = 'nicolas@elevenminds.com,backend.elevenminds@gmail.com'
        appConfig.DireccionURL = URLELEVENMINDS
        appConfig.CorreoDominioError = 'exceptionprogram.com'
        appConfig.CorreoDominioServicio = 'exceptionprogram.com'
        appConfig.DireccionLogo = '{}/{}'.format(appConfig.DireccionURL, LOGOELEVENMINDS)
        appConfig.CorreoErrores = 'errores.eleven@exceptionprogram.com'
        appConfig.CorreoSoporte = 'soporte.{}@elevenminds.com'.format(appConfig.Empresa.name.lower())
        if appConfig.Ambiente == Ambiente.Elevenminds:
            pass
        if appConfig.Ambiente == Ambiente.ElevenPruebas:
            pass
        if appConfig.Ambiente == Ambiente.BigDataTM:
            appConfig.CorreoSoporte = 'soporte.bigdatatm@elevenminds.com'
        if appConfig.Ambiente == Ambiente.BigDataTMPruebas:
            appConfig.CorreoSoporte = 'soporte.bigdatatm@elevenminds.com'
        if appConfig.Ambiente == Ambiente.Spheregt:
            appConfig.CorreoDominioServicio = 'notificaciones.spheregt.com'
            appConfig.CorreoErrores = 'errores.global@exceptionprogram.com'
            appConfig.CorreoSoporte = 'soporte.spheregt@elevenminds.com'
        if appConfig.Ambiente == Ambiente.SpheregtPruebas:
            appConfig.CorreoErrores = 'errores.global@exceptionprogram.com'
        if appConfig.Ambiente == Ambiente.CoSoAVL:
            appConfig.CorreoSoporte = 'soporte.cosoavl@elevenminds.com'
        if appConfig.Ambiente == Ambiente.CoSoAVLPruebas:
            pass
        if appConfig.Ambiente == Ambiente.SpheregtC4SanPedro:
            appConfig.CorreoSoporte = 'soporte.c4sanpedro@elevenminds.com'
        if appConfig.Ambiente == Ambiente.SpheregtC4SanPedroPruebas:
            pass
        if appConfig.Ambiente == Ambiente.BigDataTMSigma:
            appConfig.CorreoSoporte = 'soporte.sigma@elevenminds.com'
        if appConfig.Ambiente == Ambiente.BigDataTMSigmaPruebas:
            pass
        if appConfig.Ambiente == Ambiente.BigDataTMLaEuropea:
            appConfig.CorreoSoporte = 'soporte.laeurpea@elevenminds.com'
        if appConfig.Ambiente == Ambiente.BigDataTMLaEuropeaPruebas:
            pass
        if appConfig.Ambiente == Ambiente.SpheregtFiscalia:
            appConfig.CorreoDominioServicio = 'fiscalianl.gob.mx'
            appConfig.CorreoErrores = 'errores.fnl@exceptionprogram.com'
            appConfig.CorreoSoporte = 'soporte.fnl@elevenminds.com'
        if appConfig.Ambiente == Ambiente.SpheregtFiscaliaPruebas:
            pass
        if appConfig.Ambiente == Ambiente.LinkerWeb:
            appConfig.CorreoDominioError = 'linkerweb.mx'
            appConfig.CorreoSoporte = 'soporte.innova@elevenminds.com'
        if appConfig.Ambiente == Ambiente.LinkerWebRespaldo:
            appConfig.CorreoDominioError = 'linkerweb.mx'
            appConfig.CorreoSoporte = 'soporte.innova@elevenminds.com'
        if appConfig.Ambiente == Ambiente.LinkerWebPruebas:
            appConfig.CorreoDominioError = 'linkerweb.mx'
        if appConfig.Ambiente == Ambiente.LinkerWebRespaldoPruebas:
            appConfig.CorreoDominioError = 'linkerweb.mx'
        if appConfig.Ambiente == Ambiente.Naanix:
            appConfig.DireccionURL = 'https://naanix.com'
            appConfig.DireccionLogo = '{}/img/iconos_generales/logotipo_naanix_254_80.png'.format(appConfig.DireccionURL)
            appConfig.CorreoDominioServicio = 'notificaciones.rastreogps.com'
            appConfig.CorreoErrores = 'errores.sis@exceptionprogram.com'
            appConfig.CorreoSoporte = 'soporte@tecnologiasis.com'
            appConfig.Dominio = 'naanix.com'
        if appConfig.Ambiente == Ambiente.NaanixPruebas:
            appConfig.DireccionURL = 'https://naanix.com'
            appConfig.DireccionLogo = '{}/img/iconos_generales/logotipo_naanix_254_80.png'.format(appConfig.DireccionURL)
            appConfig.CorreoErrores = 'errores.sis@exceptionprogram.com'
            appConfig.CorreoSoporte = 'soporte@tecnologiasis.com'
            appConfig.Dominio = 'naanix.com'
        if appConfig.Ambiente == Ambiente.TRCM:
            appConfig.DireccionURL = 'https://rastreo.trcm.com.mx'
            appConfig.CorreoDominioServicio = 'bigdatatm.com'
            appConfig.CorreoErrores = 'errores.TRCM@exceptionprogram.com'
            appConfig.CorreoSoporte = 'soporte.trcm@elevenminds.com'
        if appConfig.Ambiente == Ambiente.TRCMPruebas:
            appConfig.DireccionURL = 'https://rastreo.trcm.com.mx'
            appConfig.CorreoErrores = 'errores.TRCM@exceptionprogram.com'
            appConfig.CorreoSoporte = 'soporte.trcm@elevenminds.com'
        appConfig.CorreoQueEnviaErrores = 'errores.{}@{}'.format(appConfig.NombreServicio.lower(), appConfig.CorreoDominioError)
        appConfig.CorreoQueEnviaServicio = 'servicio.{}@{}'.format(appConfig.NombreServicio.lower(), appConfig.CorreoDominioServicio)
        resultado = True
    except:
        GetExcept()
    finally:
        return resultado


def ConfigurarDBConnection(_DicPropiedades: dict) -> bool:
    """
        Obtiene las configuraciones de conexion a bd.
    """
    global appConfig
    resultado = False
    try:
        appConfig.ServidoresBD = {
            key: {
                'Manejador': int(value['Manejador']),
                'Tipo': int(value['Tipo']),
                'Ip': ObtenerIP(value['Ip']),
                'Puerto': int(value['Puerto']),
                'BD': Decrypt(value['BD']),
                'Usuario': Decrypt(value['Usuario']),
                'Contrasena': Decrypt(value['Contrasena']),
                'NumeroConexiones': int(value['NumeroConexiones']),
            }
            for key, value in _DicPropiedades['ServidoresBD'].items()
        }
        resultado = True
    except:
        GetExcept()
    finally:
        return resultado


def ConfigurarDBReplicas(_DicPropiedades: dict) -> bool:
    """
        Obtiene las configuaraciones para bd de replicas.
    """
    global appConfig
    resultado = False
    try:
        appConfig.ServidoresBDR = [
            {
                'Replica': int(value['Replica']),
                'TipoReplica': int(value['TipoReplica']),
                'Nombre': Decrypt(value['Nombre']),
                'Ip': ObtenerIP(value['Ip']),
                'Puerto': int(value['Puerto']),
                'BD': Decrypt(value['BD'])
            }
            for value in _DicPropiedades['ServidoresBDR']
        ]
        resultado = True
    except:
        GetExcept()
    finally:
        return resultado


def ConfigurarSmtp(_DicPropiedades: dict) -> bool:
    """
        Obtiene la configuracion de los servidores de correo.
    """
    global appConfig
    resultado = False
    try:
        appConfig.ServidoresSMTP = [
            {
                'Ip': ObtenerIP(value['Ip']),
                'Puerto': int(value['Puerto']),
                'TipoEnvio': int(value['TipoEnvio'])
            }
            for value in _DicPropiedades['ServidoresSMTP']
        ]
        resultado = True
    except:
        GetExcept()
    finally:
        return resultado


def Inicia(_Tipo: Servicio, _DicPropiedades: dict, _Validar: bool = True) -> bool:
    """
        Configura la aplicacion regresa un booleano si se hizo correctamente o no.
    """
    resultado = False
    try:
        global appConfig
        try:
            locale.setlocale(locale.LC_ALL, ('es_MX', 'UTF-8'))
        except:
            pass
        appConfig.TipoServicio = _Tipo
        appConfig.IPEquipo = ObtenerDireccionIP()
        appConfig.NombreEquipo = gethostname()
        if _Validar:
            IP = str(ObtenerIP64(appConfig.IPEquipo))
            IP64Config = str(_DicPropiedades[IP])
            if IP64Config is None:
                return
            # appConfig.IPBD = int(IP64Config)
        try:
            appConfig.Empresa = Empresa(_DicPropiedades['Empresa'])
            if _DicPropiedades['APP_EM'] == 0:
                appConfig.Ambiente = Ambiente.NoConfigurado
            elif _DicPropiedades['APP_EM'] > 0:
                appConfig.Ambiente = Ambiente((100 * appConfig.Empresa.value) + _DicPropiedades['APP_EM'])
            else:
                appConfig.Ambiente = Ambiente((-100 * appConfig.Empresa.value) + _DicPropiedades['APP_EM'])
        except:
            appConfig.Empresa = Empresa.NoConfigurado
            appConfig.Ambiente = Ambiente.NoConfigurado
        appConfig.NombreServicio = 'Backend'
        try:
            appConfig.IdServicio = int(_DicPropiedades['IdServicio']) if 'IdServicio' in _DicPropiedades else 0
            appConfig.IdInstalacion = int(_DicPropiedades['IdInstalacion']) if 'IdInstalacion' in _DicPropiedades else 0
            appConfig.InicioDinamico = bool(_DicPropiedades['InicioDinamico']) if 'InicioDinamico' in _DicPropiedades else False
            appConfig.EnviaTelegram = bool(_DicPropiedades['ET']) if 'ET' in _DicPropiedades else False
            appConfig.EnviaCorreo = bool(_DicPropiedades['EC']) if 'EC' in _DicPropiedades else False
            appConfig.NombreServicio = str(_DicPropiedades['NS']) if 'NS' in _DicPropiedades else ''
            appConfig.Descripcion = str(_DicPropiedades['DS']) if 'DS' in _DicPropiedades else ''
            appConfig.Destinatarios = list(_DicPropiedades['Destinatarios']) if 'Destinatarios' in _DicPropiedades else []
            appConfig.DestinatariosCopia = list(_DicPropiedades['Copia']) if 'Copia' in _DicPropiedades else []
            appConfig.DestinatariosCopiaOculta = list(_DicPropiedades['CopiaOculta']) if 'CopiaOculta' in _DicPropiedades else []
            appConfig.Version = str(_DicPropiedades['Version']) if 'Version' in _DicPropiedades else "0.1.1"
            appConfig.HTTP = dict(_DicPropiedades['HTTP']) if 'HTTP' in _DicPropiedades else {'Ip': 0, 'Puerto': 0}
            appConfig.WS = dict(_DicPropiedades['WS']) if 'WS' in _DicPropiedades else {'Ip': 0, 'Puerto': 0}
            appConfig.UDP = dict(_DicPropiedades['UDP']) if 'UDP' in _DicPropiedades else {'Ip': 0, 'PuertoEscucha': 0, 'PuertoEnvia': 0}
            appConfig.FuncionesBD = dict(_DicPropiedades['FuncionesBD']) if 'FuncionesBD' in _DicPropiedades else {}
            appConfig.Log = bool(_DicPropiedades['Log']) if 'Log' in _DicPropiedades else False
            appConfig.Log = bool(_DicPropiedades['LogMemoria']) if 'LogMemoria' in _DicPropiedades else False
            appConfig.Variables = dict(_DicPropiedades['Variables']) if 'Variables' in _DicPropiedades else {}
        except:
            GetExcept()
            return
        if appConfig.HTTP['Ip'] is None:
            appConfig.HTTP['Ip'] = ObtenerDireccionIP()
        else:
            ip = ObtenerIP(appConfig.HTTP['Ip'])
            if ip in ObtenerIPs() or ip == '0.0.0.0':
                appConfig.HTTP['Ip'] = ip
            else:
                return
        if appConfig.WS['Ip'] == 0:
            appConfig.WS['Ip'] = ObtenerDireccionIP()
        else:
            ip = ObtenerIP(appConfig.WS['Ip'])
            if ip in ObtenerIPs():
                appConfig.WS['Ip'] = ip
            else:
                return
        if appConfig.UDP['Ip'] == 0:
            appConfig.UDP['Ip'] = ObtenerDireccionIP()
        else:
            ip = ObtenerIP(appConfig.UDP['Ip'])
            if ip in ObtenerIPs():
                appConfig.UDP['Ip'] = ip
            else:
                return
        empresa = '' if _DicPropiedades['APP_EM'] > 0 else '{}/'.format(appConfig.Empresa.name.lower())
        if 'DL' in _DicPropiedades:
            appConfig.DirectorioLog = _DicPropiedades['DL']
            appConfig.DirectorioLogServicio = '{}/logs/{}{}/{}_{}_{}'.format(
                _DicPropiedades['DL'], empresa, appConfig.Ambiente.name.lower(), appConfig.IdServicio, appConfig.IdInstalacion, appConfig.NombreServicio
            )
            CrearDirectorio(appConfig.DirectorioLogServicio)
            appConfig.IdInicio = LogInicio(appConfig.InicioDinamico, appConfig.DirectorioLogServicio, appConfig.Empresa.name, appConfig.Ambiente.name)
            appConfig.DirectorioLogServicio = '{}/{}_Inicio'.format(appConfig.DirectorioLogServicio, appConfig.IdInicio)
            CrearDirectorio(appConfig.DirectorioLogServicio)
            appConfig.DirectorioSql = '{}/sql/{}{}/{}_{}_{}'.format(
                _DicPropiedades['DL'], empresa, appConfig.Ambiente.name.lower(), appConfig.IdServicio, appConfig.IdInstalacion, appConfig.NombreServicio
            )
            CrearDirectorio(appConfig.DirectorioSql)
        if 'DA' in _DicPropiedades:
            appConfig.DirectorioArc = _DicPropiedades['DA']
            appConfig.DirectorioAlerta = '{}/archivos/{}{}/{}_{}_{}/Alertas'.format(
                _DicPropiedades['DA'], empresa, appConfig.Ambiente.name.lower(), appConfig.IdServicio, appConfig.IdInstalacion, appConfig.NombreServicio
            )
            CrearDirectorio(appConfig.DirectorioAlerta)
            appConfig.DirectorioArchivo = '{}/archivos/{}{}/{}_{}_{}/Archivos'.format(
                _DicPropiedades['DA'], empresa, appConfig.Ambiente.name.lower(), appConfig.IdServicio, appConfig.IdInstalacion, appConfig.NombreServicio
            )
            CrearDirectorio(appConfig.DirectorioArchivo)
            appConfig.DirectorioPlantilla = '{}/archivos/{}{}/{}_{}_{}/Plantillas'.format(
                _DicPropiedades['DA'], empresa, appConfig.Ambiente.name.lower(), appConfig.IdServicio, appConfig.IdInstalacion, appConfig.NombreServicio
            )
            CrearDirectorio(appConfig.DirectorioPlantilla)
        if appConfig.IdInicio == 0:
            return
        if not ConfiguracionAmbiente():
            return
        if not StartSecurity(appConfig):
            return
        if not (ConfigurarDBConnection(_DicPropiedades) if 'ServidoresBD' in _DicPropiedades else True):
            return
        if not (ConfigurarDBReplicas(_DicPropiedades) if 'ServidoresBDR' in _DicPropiedades else True):
            return
        if not (ConfigurarSmtp(_DicPropiedades) if 'ServidoresSMTP' in _DicPropiedades else True):
            return
        resultado = True
    except:
        GetExcept()
        resultado = False
    finally:
        return resultado


def ObtenerConfiguracion(_Direccion: str) -> dict or None:
    """
        lee el archivo de confifguracion de app.json
    """
    resultado = None
    try:
        with open(_Direccion, 'r') as file:
            resultado = load(file)
    except:
        GetExcept()
    finally:
        return resultado


def MensajePrecaucion(_TipoMensaje: Evento, _Metodo: str, _Mensaje: str, _MensajeError: Exception = None) -> None:
    """
        Imprime un mesaje de color en la consola.
    """
    if _TipoMensaje == Evento.Error:
        color = Fore.RED
        tipo = 'Precaución'
    elif _TipoMensaje == Evento.Alerta:
        color = Fore.YELLOW
        tipo = 'Advertencia'
    else:
        color = Fore.CYAN
        tipo = 'Información'
    print('{}{}{} {}: {} - {}'.format(Style.BRIGHT, color, str_FechaHora(datetime.utcnow()), tipo, _Metodo, _Mensaje))
    if not _MensajeError is None:
        print(_MensajeError)
    print(Style.RESET_ALL)


def MensajeLog(_TipoLog: Evento, _Metodo: str, _Mensaje: str) -> None:
    """
        Imprime un mensaje de color en la consola
    """
    if _TipoLog == Evento.Error:
        color = Fore.RED
        tipo = 'Precaución'
    elif _TipoLog == Evento.Alerta:
        color = Fore.YELLOW
        tipo = 'Advertencia'
    else:
        color = Fore.CYAN
        tipo = 'Información'
    print('{}{}{} {}: {} - {}'.format(Style.BRIGHT, color, str_FechaHora(datetime.utcnow()), tipo, _Metodo, _Mensaje))
