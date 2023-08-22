from backend.archivo import LogProceso
from backend.configuracion import appConfig, Inicia, ObtenerConfiguracion, MensajePrecaucion
from backend.entidades import Servicio, Evento
from backend.logger import CorreoSendStart, TelegramSendStart
from datetime import datetime
from datos.conexion import IniciarConexion
from memorias.memoria import Diccionarios as memoriaGeneral, IniciarMemoria
from servicios.rest import IniciarRest
from sys import exit
from utilidades.mas import IniciarClienteMAS


if __name__ == '__main__':
    dicPropiedades = ObtenerConfiguracion('app.json')
    if dicPropiedades is None:
        MensajePrecaucion(Evento.Error, 'ObtenerConfiguracion()', 'El Servicio no iniciara por que no se ha configurado correctamente 1.', None)
        exit(0)
    if not Inicia(Servicio.Servicio, dicPropiedades, False):
        MensajePrecaucion(Evento.Error, 'Iniciar()', 'El Servicio no iniciara por que no se ha configurado correctamente 2.', None)
        exit(0)
    try:
        dateutc = datetime.utcnow()
        IniciarConexion()
        LogProceso(appConfig.DirectorioLogServicio, datetime.utcnow() - dateutc, 'IniciarConexion', 'La conexion a la bd se hizo correctamente.')
        dateutc = datetime.utcnow()
        IniciarMemoria()
        LogProceso(appConfig.DirectorioLogServicio, datetime.utcnow() - dateutc, 'IniciarMemoria', 'La memoria se cargo correctamente.')
        dateutc = datetime.utcnow()
        IniciarRest()
        LogProceso(appConfig.DirectorioLogServicio, datetime.utcnow() - dateutc, 'IniciarRest', 'El servicio rest se ha iniciado correctamente.')
        # fechaUtc = datetime.utcnow()
        # IniciarClienteMAS()
        # LogProceso(appConfig.DirectorioLogServicio,  datetime.utcnow() - fechaUtc, 'Iniciar MAS', 'El servicio MASClient se inicio correctamente.')
        # CorreoSendStart()
        TelegramSendStart()
    except Exception as e:
        MensajePrecaucion(Evento.Error, 'Start()', 'No se pudo iniciar el servicio', e)
        exit(0)