from backend.entidades import Correo, EnvioCorreo, Evento, Metodo, MimeType, Orientacion, Tabla, Telegram
from backend.fecha import str_Fecha, str_FechaHora, UtcToCentro
from backend.telegram import EscapeCharacters, SendMessage
from backend.archivo import CrearDirectorio, ExisteArchivo
from backend.basic import GetExcept as GetExcept2
from backend.configuracion import appConfig
from backend.correo import EnviarCorreo
from backend.html import CrearHTML
from backend.ip import ObtenerIPs
from csv import writer, QUOTE_ALL
from datetime import datetime
from os.path import split
import sys


def WriteLog(_Event: Evento, _Py: str, _Method: str, _Info: str) -> None:
    """
        Escribe en un archivo la informacion que se proporciona.
        _Event: INFORMACION, ERROR O CRITICO
        _Py: Nombre del script
        _Method: Nombre del metodo
        _Info: Informacion para guardar
    """
    try:
        fecha = datetime.utcnow()
        day, hour = str_Fecha(fecha), fecha.strftime('%H:%M:%S')
        filename = '{}/{}_{}.log'.format(appConfig.DirectorioLogServicio, day, _Event.name)
        with open(filename, 'a') as file:
            file.write('{} {} {} {}\n'.format(hour, _Py, _Method, _Info))
    except:
        GetExcept2()


def TelegramSendEnd(_Method: Metodo, _Message='', _Send=True) -> None:
    """
        Crea el formato de texto para enviar la informacion del final de un servicio en telegram.
    """
    try:
        message = '*Ambiente:* \#{}\n'.format(EscapeCharacters(appConfig.Ambiente.name))
        message += '*Servicio:* \#{}\n'.format(EscapeCharacters(appConfig.NombreServicio))
        message += '*Instancia:* `{} | {}`\n'.format(EscapeCharacters(appConfig.IdServicio), EscapeCharacters(appConfig.IdInstalacion))
        port = ''
        if _Method == Metodo.Rest:
            port = ':{}'.format(EscapeCharacters(appConfig.HTTP['Puerto']))
        if _Method == Metodo.WebSocket:
            port = ':{}'.format(EscapeCharacters(appConfig.WS['Puerto']))
        if _Method == Metodo.Udp:
            port = ':{}'.format(EscapeCharacters(appConfig.UDP['PuertoEnvia'] if _Send else appConfig.UDP['PuertoEscucha']))
        message += '*Instalado:* `{}` \(`{}{}`\)\n'.format(EscapeCharacters(appConfig.NombreEquipo), EscapeCharacters(appConfig.IPEquipo), port)
        message += '*Version:* `{}`\n'.format(EscapeCharacters(appConfig.Version))
        message += '*Metodo:* `{}`\n'.format(EscapeCharacters(_Method.name))
        if _Message != '':
            message += '*Mensaje:* `{}`\n'.format(EscapeCharacters(_Message))
        SendMessage(message, Telegram.Advertencias, _Method='TelegramSendEnd')
    except:
        GetExcept2()


def TelegramSendError(_Function: str, _Line: str, _Error: str, _Method: Metodo, _Message='', _Link='', _Send=True) -> None:
    """
        Crea el formato de texto para enviar la informacion del error en telegram.
    """
    try:
        message = '❗️ *{} Error de Servicio*\n'.format(EscapeCharacters(appConfig.NombreServicio))
        message += '*Clave:* \#Bigdatatm \#{} \#{}T{} \#{}\n'.format(
            EscapeCharacters(appConfig.Ambiente.name), appConfig.IdServicio, appConfig.IdInstalacion, EscapeCharacters(appConfig.NombreServicio)
        )
        message += '*Servidor:* `{}` \(`{}`\)\n'.format(EscapeCharacters(appConfig.NombreEquipo), EscapeCharacters(', '.join(ObtenerIPs())))
        message += '*Fecha:* `{}`\n'.format(EscapeCharacters(str(str_FechaHora(UtcToCentro(datetime.utcnow())))))
        message += '*Mensaje:* `Se ha detectado un error en el servicio`\n\n'
        port = ''
        if _Method == Metodo.Rest:
            port = '{}:{}'.format(EscapeCharacters(appConfig.HTTP['Ip']), EscapeCharacters(appConfig.HTTP['Puerto']))
        if _Method == Metodo.WebSocket:
            port = '{}:{}'.format(EscapeCharacters(appConfig.WS['Ip']), EscapeCharacters(appConfig.WS['Puerto']))
        if _Method == Metodo.Udp:
            port = '{}:{}'.format(EscapeCharacters(appConfig.UDP['Ip']), EscapeCharacters(appConfig.UDP['PuertoEnvia'] if _Send else appConfig.UDP['PuertoEscucha']))
        if port != '':
            message += '*UrlLocal:* `{}`\n'.format(port)
        message += '*Version:* `{}`\n'.format(EscapeCharacters(appConfig.Version))
        message += '*Metodo:* `{}`\n'.format(EscapeCharacters(_Method.name))
        message += '*Funcion:* `{}`\n'.format(EscapeCharacters(_Function))
        message += '*Error:* `{}`\n'.format(EscapeCharacters(_Error))
        message += '*Linea:* `{}`\n'.format(EscapeCharacters(_Line))
        if _Message != '':
            message += '*Mensaje:* `{}`\n'.format(EscapeCharacters(_Message))
        if _Link != '':
            message += '*Link:* {}\n'.format(_Link)
        SendMessage(message, _Method='TelegramSendError')
    except:
        GetExcept2()


def TelegramSendStart() -> None:
    """
        Crea el formato de texto para enviar la informacion del inicio del servicio.
    """
    try:
        message = '🔔 *{} Alerta de Inicio*\n'.format(EscapeCharacters(appConfig.NombreServicio))
        message += '*Clave:* \#Bigdatatm \#{} \#{}T{} \#{}\n'.format(
            EscapeCharacters(appConfig.Ambiente.name), appConfig.IdServicio, appConfig.IdInstalacion, EscapeCharacters(appConfig.NombreServicio)
        )
        message += '*Servidor:* `{}` \(`{}`\)\n'.format(EscapeCharacters(appConfig.NombreEquipo), EscapeCharacters(', '.join(ObtenerIPs())))
        message += '*Fecha:* `{}`\n'.format(EscapeCharacters(str(str_FechaHora(UtcToCentro(datetime.utcnow())))))
        message += '*Mensaje:* `El servicio se ha iniciado`\n\n'
        message += '*Descripcion:* `{}`\n'.format(EscapeCharacters(appConfig.Descripcion))
        message += '*Version:* `{}`\n'.format(EscapeCharacters(appConfig.Version))
        if appConfig.HTTP['Puerto'] != 0:
            message += '*Puerto http:* `{}:{}`\n'.format(EscapeCharacters(appConfig.HTTP['Ip']), EscapeCharacters(appConfig.HTTP['Puerto']))
        if appConfig.WS['Puerto'] != 0:
            message += '*Puerto ws:* `{}:{}`\n'.format(EscapeCharacters(appConfig.WS['Ip']), EscapeCharacters(appConfig.WS['Puerto']))
        if appConfig.UDP['PuertoEscucha'] != 0:
            message += '*Puerto udp escucha:* `{}:{}`\n'.format(EscapeCharacters(appConfig.UDP['Ip']), EscapeCharacters(appConfig.UDP['PuertoEscucha']))
        if appConfig.UDP['PuertoEnvia'] != 0:
            message += '*Puerto udp envia:* `{}:{}`\n'.format(EscapeCharacters(appConfig.UDP['Ip']), EscapeCharacters(appConfig.UDP['PuertoEnvia']))
        SendMessage(message, Telegram.Alertas, _Method='TelegramSendStart')
    except:
        GetExcept2()


def CorreoSendError(_Function: str, _Line: str, _Error: str, _Method: Metodo, _Message='', _Send=True) -> None:
    """
        Crea el formato de texto para enviar la informacion del inicio del servicio.
    """
    try:
        encabezados = ['Ambiente', 'Servicio', 'Instancia', 'Instalado', 'Version', 'Metodo', 'Funcion', 'Error', 'Linea']
        port = ', '.join(ObtenerIPs())
        if _Method == Metodo.Rest:
            port = '{}:{}'.format(appConfig.HTTP['Ip'], appConfig.HTTP['Puerto'])
        if _Method == Metodo.WebSocket:
            port = '{}:{}'.format(appConfig.WS['Ip'], appConfig.WS['Puerto'])
        if _Method == Metodo.Udp:
            port = '{}:{}'.format(appConfig.UDP['Ip'], appConfig.UDP['PuertoEnvia'] if _Send else appConfig.UDP['PuertoEscucha'])
        data = [
            appConfig.Ambiente.name, appConfig.NombreServicio, '{} | {}'.format(appConfig.IdServicio, appConfig.IdInstalacion),
            '{} ({})\n'.format(appConfig.NombreEquipo, port), appConfig.Version, _Method.name, _Function, _Error, _Line
        ]
        if _Message != '':
            encabezados.append('Mensaje')
            data.append(_Message)
        encabezados.append('Fecha')
        data.append(str_FechaHora(UtcToCentro(datetime.utcnow()), 12))
        listTable = [
            Tabla('Error del servicio: {} '.format(appConfig.NombreServicio), '', encabezados, [data], Orientacion.Horizontal, EnvioCorreo.Error)
        ]
        html = CrearHTML(listTable, '', True, True, True, True)
        EnviarCorreo(
            Correo.Error, '{} {} {}'.format(appConfig.Ambiente.name, appConfig.NombreServicio, _Function.split(' ')[1]), html, 'Errores {}'.format(appConfig.NombreCorreo),
            appConfig.CorreoQueEnviaErrores, [appConfig.CorreoErrores], [], [], MimeType.Html
        )
    except:
        GetExcept2()


def CorreoSendStart() -> None:
    """
        Crea el formato de texto para enviar la informacion del inicio del servicio.
    """
    try:
        encabezados = ['Ambiente', 'Servicio', 'Instancia', 'Descripcion', 'Instalado', 'Version']
        data = [
            appConfig.Ambiente.name, appConfig.NombreServicio, '{} | {}'.format(appConfig.IdServicio, appConfig.IdInstalacion),
            appConfig.Descripcion, '{} ({})\n'.format(appConfig.NombreEquipo, ', '.join(ObtenerIPs())), appConfig.Version
        ]
        if appConfig.HTTP['Puerto'] != 0:
            encabezados.append('Puerto http')
            data.append('{}:{}'.format(appConfig.HTTP['Ip'], appConfig.HTTP['Puerto']))
        if appConfig.WS['Puerto'] != 0:
            encabezados.append('Puerto ws')
            data.append('{}:{}'.format(appConfig.WS['Ip'], appConfig.WS['Puerto']))
        if appConfig.UDP['PuertoEscucha'] != 0:
            encabezados.append('Puerto udp escucha')
            data.append('{}:{}'.format(appConfig.UDP['Ip'], appConfig.UDP['PuertoEscucha']))
        if appConfig.UDP['PuertoEnvia'] != 0:
            encabezados.append('Puerto udp envia')
            data.append('{}:{}'.format(appConfig.UDP['Ip'], appConfig.UDP['PuertoEnvia']))
        encabezados.append('Fecha')
        data.append(str_FechaHora(UtcToCentro(datetime.utcnow()), 12))
        listTable = [
            Tabla('Inicio del servicio: {} '.format(appConfig.NombreServicio), '', encabezados, [data], Orientacion.Horizontal, EnvioCorreo.Notificacion)
        ]
        html = CrearHTML(listTable, '', True, True, True, True)
        EnviarCorreo(
            Correo.Error, '{} {} Inicio'.format(appConfig.Ambiente.name, appConfig.NombreServicio), html, 'Alertas {}'.format(appConfig.NombreCorreo),
            appConfig.CorreoQueEnviaErrores, [appConfig.CorreoErrores], [], [], MimeType.Html
        )
        EnviarCorreo(
            Correo.Normal, '{} {} Inicio'.format(appConfig.Ambiente.name, appConfig.NombreServicio), html, 'Alertas {}'.format(appConfig.NombreCorreo),
            appConfig.CorreoQueEnviaServicio, appConfig.Destinatarios, appConfig.DestinatariosCopia, appConfig.DestinatariosCopiaOculta, MimeType.Html
        )
    except:
        GetExcept2()


def GetExcept(_Error=Evento.Error, _Method=Metodo.Proceso, _Message='', _Link='', _Email=True, _Telegram=True, _Log=True, _Send=True) -> None:
    """
        Obtiene los detalles del error para escribirlos a
        un log y enviarlos por telegram si esta disponible.
    """
    try:
        errorType, errorMessage, exc_tb = sys.exc_info()
        errorFile = split(exc_tb.tb_frame.f_code.co_filename)[1]
        errorLine = exc_tb.tb_lineno
        errorMethod = '{}()'.format(exc_tb.tb_frame.f_code.co_name)
        if _Error in (Evento.Critico, Evento.Error):
            if _Log:
                WriteLog(_Error, errorFile, errorMethod, '{} {} {} {}'.format(errorLine, errorType, errorMessage, _Message))
            if appConfig.EnviaTelegram and _Telegram:
                TelegramSendError('{} {}'.format(errorFile, errorMethod), errorLine, '{} {}'.format(errorType, errorMessage), _Method, _Message, _Link, _Send)
            if appConfig.EnviaCorreo and _Email:
                CorreoSendError('{} {}'.format(errorFile, errorMethod), errorLine, '{} {}'.format(errorType, errorMessage), _Method, _Message, _Send)
    except:
        GetExcept2()


def LogErrores(_Class: str, _Name: str, _Date: datetime, _Function: str, _Error: str, _InnerExcepption = '', _StrackTrace = '', _Source = '', _Query = '', _Connection = '') -> None:
    """
        Crea un log de error para las consultas de postgresql.
    """
    try:
        fecha = datetime.utcnow()
        day = str_Fecha(fecha)
        direct = '{}/{}'.format(appConfig.DirectorioLogServicio, day)
        CrearDirectorio(direct)
        fileName = '{}/{}_Errores_{}_{}.csv'.format(direct, fecha.hour, _Class, _Name).replace(' ', '_')
        if not ExisteArchivo(fileName):
            with open(fileName, 'w') as f:
                f.write('"Fecha","Funcion","Nombre","Error","InnerException","StackTrace","Source","Query","Conexion"\n')
        if _Query != '':
            CrearDirectorio(fileName[:-4])
            fileName2 = '{}/{}_{}.sql'.format(fileName[:-4], str_FechaHora(fecha), _Function).replace(' ', '_')
            with open(fileName2, 'a') as f:
                f.write(_Query)
            _Query = fileName2
        with open(fileName, 'a') as f:
            c = writer(f, delimiter=',', quotechar='"', quoting=QUOTE_ALL)
            c.writerow([str_FechaHora(_Date), _Function, _Name, _Error, _InnerExcepption, _StrackTrace, _Source, _Query, _Connection])
    except:
        GetExcept2()
