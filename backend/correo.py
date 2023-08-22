from backend.entidades import Correo, MimeType, Mensaje
from email.mime.multipart import MIMEMultipart
from backend.configuracion import appConfig
from email.encoders import encode_base64
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from backend.basic import GetExcept
from random import choice
from smtplib import SMTP


ultimoServidor = {0: {}, 1: {}}


def SeleccionarServidor(_Tipo: int) -> dict or None:
    """
        Selecciona una configuracion de servidor distinta a la
        anterior, en el caso de haber mas de una configuracion.
    """
    global ultimoServidor
    try:
        lista = [item for item in appConfig.ServidoresSMTP if item['TipoEnvio'] == _Tipo]
        if len(lista) == 1:
            ultimoServidor[_Tipo] = lista[0]
        else:
            if ultimoServidor[_Tipo] == {}:
                ultimoServidor[_Tipo] = lista[0]
            else:
                lista2 = [
                    item
                    for item in lista
                    if item['Ip'] != ultimoServidor[_Tipo]['Ip'] or item['Puerto'] != ultimoServidor[_Tipo]['Puerto']
                ]
                ultimoServidor[_Tipo] = choice(lista2)
        return ultimoServidor[_Tipo]
    except:
        GetExcept(_Message=appConfig.ServidoresSMTP)
        return None


def Enviar(_Tipo: Correo, _Mensaje: Mensaje) -> bool:
    """
        Envia un correo electronico.
    """
    resultado = False
    try:
        servidor = SeleccionarServidor(_Tipo.value)
        smpt = SMTP(servidor['Ip'], servidor['Puerto'])
        smpt.sendmail(_Mensaje.De, _Mensaje.Para, _Mensaje.Datos.as_string())
        smpt.quit()
        resultado = True
    except:
        GetExcept()
    finally:
        return resultado


def Enviar2(_ServidorIp: str, _ServidorPuerto: int, _Mensaje: Mensaje) -> None or Exception:
    """
        Envia un correo electronico.
    """
    try:
        smpt = SMTP(_ServidorIp, _ServidorPuerto)
        smpt.sendmail(_Mensaje.De, _Mensaje.Para, _Mensaje.Datos.as_string())
        smpt.quit()
        return None
    except Exception as e:
        return e


def EnviarCorreo(_Tipo: Correo, _Asunto: str, _Mensaje: str, _NombreCorreo: str, _CorreoEnvia: str, _Destinatario: list, _ConCopia: list, _ConCopiaOculta: list, _TipoTexto: MimeType, _Archivos: list=[], _NombreArchivos:list=[]) -> bool:
    """
        Envia un correo de forma normal.
    """
    resultado = False
    try:
        msg = MIMEMultipart()
        msg['From'] = '{}<{}>'.format(_NombreCorreo, _CorreoEnvia)
        msg['To'] = ','.join(_Destinatario)
        msg['Cc'] = ','.join(_ConCopia)
        msg['Cco'] = ','.join(_ConCopiaOculta)
        msg['Subject'] = _Asunto
        msg.attach(MIMEText(_Mensaje, _TipoTexto.name))
        for x in range(len(_Archivos)):
            with open(_Archivos[x], 'rb') as file:
                f = MIMEBase('application', 'octet-stream')
                f.set_payload(file.read())
            encode_base64(f)
            f.add_header('content-disposition', 'attachment;filename={}'.format(_NombreArchivos[x]))
            msg.attach(f)
        mensaje = Mensaje()
        mensaje.De = _CorreoEnvia
        mensaje.Para = _Destinatario + _ConCopia + _ConCopiaOculta
        mensaje.Datos = msg
        resultado = Enviar(_Tipo, mensaje)
    except:
        GetExcept()
    finally:
        return resultado


def EnviarCorreo2(_ServidorIp: str, _ServidorPuerto: int, _Asunto: str, _Mensaje: str, _NombreCorreo: str, _CorreoEnvia: str, _Destinatario: list, _ConCopia: list, _ConCopiaOculta: list, _Archivos: list, _NombreArchivos, _TipoTexto: MimeType) -> None or Exception:
    """
        Envia un correo de forma normal.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = '{}<{}>'.format(_NombreCorreo, _CorreoEnvia)
        msg['To'] = ','.join(_Destinatario)
        msg['Cc'] = ','.join(_ConCopia)
        msg['Cco'] = ','.join(_ConCopiaOculta)
        msg['Subject'] = _Asunto
        msg.attach(MIMEText(_Mensaje, _TipoTexto))
        for x in range(len(_Archivos)):
            with open(_Archivos[x], 'rb') as file:
                f = MIMEBase('application', 'octet-stream')
                f.set_payload(file.read())
            encode_base64(f)
            f.add_header('content-disposition', 'attachment;filename={}'.format(_NombreArchivos[x]))
            msg.attach(f)
        mensaje = Mensaje()
        mensaje.De = _CorreoEnvia
        mensaje.Para = _Destinatario + _ConCopia + _ConCopiaOculta
        mensaje.Datos = msg
        return Enviar2(_ServidorIp, _ServidorPuerto, mensaje)
    except Exception as e:
        return e
