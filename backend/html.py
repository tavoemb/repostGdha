from backend.entidades import EnvioCorreo, Orientacion, Tabla
from backend.configuracion import appConfig
from backend.basic import GetExcept


imagenNotificacion = "/images/Backend_Notificacion.png"
imagenError = "/images/Backend_Error2.png"
estiloFuente = "font-family:Roboto,Arial;display:inline;"
Urlelevenminds = "http://elevenminds.com"
dictColorNotificacion = {
    EnvioCorreo.Error: 'FireBrick',
    EnvioCorreo.Notificacion: 'DimGray',
    EnvioCorreo.Ok: 'SeaGreen',
    EnvioCorreo.Precaucion: 'DarkOrange',
    EnvioCorreo.Recordatorio: 'DimGray',
    EnvioCorreo.Reporte: 'DimGray',
    EnvioCorreo.Resumen: '#2e2e2e'
}


def CrearHTML(_ListaTablas: list, _MensajeAdicional: str, _PiePagina: bool, _Interno: bool, _CorreoSoporte: bool, _Ajustar: bool) -> str:
    """
        Crea la plantilla de acuerdo a los parametros proporcionados.
    """
    try:
        if _MensajeAdicional != '' or len(_ListaTablas) > 0:
            URLImagenNotificacion = '{}{}'.format(Urlelevenminds, imagenNotificacion)
            MensajeCorreoSoporte = 'Este correo es informativo, favor no responder a esta direcci&oacute;n de correo, ya que no se encuentra habilitada para recibir mensajes.'
            if _CorreoSoporte:
                MensajeCorreoSoporte += 'Si requiere mayor informaci&oacute;n sobre el contenido de este mensaje, contactar a <a href="mailto:{0}">{0}</a>'.format(appConfig.CorreoSoporte)
            html = """
                <html>
                <body>
                <table style="width: 100%; font-family: Roboto-Regular,Helvetica,Arial,sans-serif;">
                <tbody>
                <tr>
                <td>
                <table cellspacing="0" cellpadding="0" style="max-width: 90%; margin:0px auto; border: 1px solid #d6d6d6; overflow: hidden; border-radius: 10px;">
                <tbody style="border-radius: 20px;">
                <tr>
                <td>
                <table cellspacing="0" cellpadding="0" width="100%">
                <tbody>
                <tr>
                <td>
            """
            for Obj in _ListaTablas:
                Obj: Tabla
                TamanioCelda = 5
                if _Ajustar:
                    TamanioCelda = 2
                Color = dictColorNotificacion[Obj.TipoNotificacion]
                if Obj.Mensaje != '':
                    html += """
                        <div>
                        <table cellspacing="0" cellpadding="5" height="100%" width="100%" style="word-break:break-word">
                        <tbody>
                        <tr style="background-color:{};color:white;font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-weight:bold;">
                        <td>
                        <table cellspacing="0" cellpadding="0" width="95%" align="center" style="color:white;;text-align:left;word-break:break-word">
                        <tbody>
                        <tr>
                        <td width="30">
                        <img src="{}" width="40" height="30" style="display:block;max-width:100%;height:auto!important"/>
                        </td>
                        <td style="padding-left:10px;">
                        <div>
                        <span style="font-size:20px;font-weight:bold;">{}</span>
                        </div>
                        </td>
                        </tr>
                        </tbody>
                        </table>
                        </td>
                        </tr>
                        <tr>
                        <td>
                        <table cellspacing="0" cellpadding="0" width="95%" align="center" style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:grey;text-align:left;word-break:break-word">
                        <tbody>
                        <tr>
                        <td style="width:100%;">{}</td>
                        </tr>
                        </tbody>
                        </table>
                        </td>
                        </tr>
                        </tbody>
                        </table>
                        </div>
                    """.format(Color, URLImagenNotificacion, Obj.Titulo, Obj.Mensaje)
                else:
                    if Obj.Orientacion == Orientacion.Vertical:
                        html += """
                            <div>
                            <table cellspacing="0" cellpadding="{}" height="100%" width="100%" style="word-break:break-word">
                            <tbody>
                            <tr style="background-color:{};color:white;font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-weight:bold;">
                            <td>
                            <table cellspacing="0" cellpadding="0" width="95%" align="center" style="color:white;;text-align:left;word-break:break-word">
                            <tbody>
                            <tr>
                            <td width="30">
                            <img src="{}" width="40" height="30" style="display:block;max-width:100%;height:auto!important"/>
                            </td>
                            <td style="padding-left:10px;">
                            <div>
                            <span style="font-size:20px;font-weight:bold;">{}</span>
                            </div>
                            </td>
                            </tr>
                            </tbody>
                            </table>
                            </td>
                            </tr>
                            <tr style="background-color:gray;color:white;font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-weight:bold;">
                            <td style="padding-top:0px;padding-bottom:0px;">
                            <table cellspacing="0" cellpadding="2" width="95%" align="center" style="color:white;text-align:left;font-size:16px;font-weight:bold;word-break:break-word">
                            <tbody>
                            <tr>
                        """.format(TamanioCelda, Color, URLImagenNotificacion, Obj.Titulo)
                        TamColumna = 100 / len(Obj.Encabezados)
                        for Encabezado in Obj.Encabezados:
                            html += """<td style="width:{}%;">{}</td>""".format(TamColumna, Encabezado)
                        html += """
                            </tr>
                            </tbody>
                            </table>
                            </td>
                            </tr>
                            <tr>
                            <td>
                            <table cellspacing="0" cellpadding="0" width="95%" align="center" style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:grey;text-align:left;word-break:break-word">
                            <tbody>
                        """
                        for Fila in Obj.Datos:
                            html += '<tr>'
                            for FilaMensaje in Fila:
                                html += '<td style="width:{}%;">{}</td>'.format(TamColumna, FilaMensaje)
                            html += '</tr>'
                        html += """
                            </tbody>
                            </table>
                            </td>
                            </tr>
                            </tbody>
                            </table>
                            </div>
                        """
                    else:
                        html += """
                            <div>
                            <table cellspacing="0" cellpadding="{}" height="100%" width="100%" style="word-break:break-word">
                            <tbody>
                            <tr style="background-color:{};color:white;font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-weight:bold;">
                            <td>
                            <table cellspacing="0" cellpadding="0" width="95%" align="center" style="color:white;;text-align:left;word-break:break-word">
                            <tbody>
                            <tr>
                            <td width="30">
                            <img src="{}" width="40" height="30" style="display:block;max-width:100%;height:auto!important"/>
                            </td>
                            <td style="padding-left:10px;">
                            <div>
                            <span style="font-size:20px;font-weight:bold;">{}</span>
                            </div>
                            </td>
                            </tr>
                            </tbody>
                            </table>
                            </td>
                            </tr>
                            <tr>
                            <td>
                            <table cellspacing="0" cellpadding="0" width="95%" align="center" style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:grey;text-align:left;word-break:break-word">
                            <tbody>
                        """.format(TamanioCelda, Color, URLImagenNotificacion, Obj.Titulo)
                        for i in range(len(Obj.Encabezados)):
                            html += """
                                <tr>
                                <td width="20%" style="font-weight:bold;font-size:14px;">{}</td>
                            """.format(Obj.Encabezados[i])
                            for Fila in Obj.Datos:
                                mensaje = ''
                                if len(Fila) > i:
                                    mensaje = Fila[i]
                                html += '<td>{}</td>'.format(mensaje)
                            html += '</tr>'
                        html += """
                            </tbody>
                            </table>
                            </td>
                            </tr>
                            </tbody>
                            </table>
                            </div>
                        """
            html += """
                <div style="border-bottom: thin solid #f0f0f0;">
                <table cellspacing="0" cellpadding="2" height="100%" width="100%" style="word-break:break-word">
                <tbody>
                <tr style="background-color:#f0f0f0;font-family:Roboto-Regular,Helvetica,Arial,sans-serif;">
                <td>
                <table cellspacing="0" cellpadding="0" width="95%" align="center" style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:12px;color:rgba(0,0,0,0.54);text-align:left;word-break:break-word;padding: 0px;">
                <tbody>
                <tr>
                <td>
                <strong>IMPORTANTE:</strong><br>{}</td>
                </tr>
                </tbody>
                </table>
                </td>
                </tr>
                </tbody>
                </table>
                </div>
                </td>
                </tr>
                </tbody>
                </table>
                </td>
                </tr>
                </tbody>
                </table>
                </td>
                </tr>
            """.format(MensajeCorreoSoporte)
            if _PiePagina:
                logo = '{}'.format(appConfig.DireccionLogo)
                if not _Interno:
                    logo = '{}'.format(appConfig.DireccionLogo)
                html += """
                    <tr>
                    <td>
                    <div style="text-align:center;">
                    <img src="{}" style="max-width: 254px; min-width:254px;  width: 254px; height: 80px; max-height: 80px; min-height:80px;"/>
                    </div>
                    </td>
                    </tr>
                """.format(logo)
            html += """
                </tbody>
                </table>
                </body>
                </html>
            """
            return html
        return ''
    except:
        GetExcept()
        return ''


def CrearHtmlImage(_ListaTablas: list, _MensajeAdicional: str) -> str:
    """
        Crea la plantilla de acuerdo a los parametros proporcionados.
    """
    try:
        if _MensajeAdicional != '' or len(_ListaTablas) > 0:
            URLImagenNotificacion = '{}{}'.format(Urlelevenminds, imagenNotificacion)
            html = """
                <!DOCTYPE html>
                <html lang="es">
                <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Message</title>
                </head>
                <body>
                <table cellspacing="0" cellpadding="0" style="width: 100%; margin:0px auto; border: 1px solid #d6d6d6; overflow: hidden; border-radius: 10px;">
                <tbody>
                <tr>
                <td>
            """
            for Obj in _ListaTablas:
                Obj: Tabla
                Color = dictColorNotificacion[Obj.TipoNotificacion]
                if Obj.Mensaje != '':
                    html += """
                        <div>
                        <table cellspacing="0" cellpadding="5" height="100%" width="100%" style="word-break:break-word">
                        <tbody style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:grey;text-align:left;word-break:break-word">
                        <tr style="background-color:{};color:white;font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-weight:bold;">
                        <td colspan="{}">
                        <p style="padding: 0px; margin: 0px;">
                        <img width="30px" height="30px" style="height:auto; padding: 0px; margin: 0px;" src="{}"/>
                        <span style="font-size:20px; font-weight:bold;">{}</span>
                        </p>
                        </td>
                        </tr>
                        <tr>
                        <td colspan="{}">
                        <p>{}</p>
                        </td>
                        </tr>
                    """.format(Color, len(Obj.Encabezados), URLImagenNotificacion, Obj.Titulo, len(Obj.Encabezados), Obj.Mensaje)
                else:
                    if Obj.Orientacion == Orientacion.Vertical:
                        html += """
                            <div>
                            <table cellspacing="0" cellpadding="5" height="100%" width="100%" style="word-break:break-word">
                            <tbody style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:grey;text-align:left;word-break:break-word">
                            <tr style="background-color:{};color:white;font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-weight:bold;">
                            <td colspan="{}">
                            <p style="padding: 0px; margin: 0px;">
                            <img width="30px" height="30px" style="height:auto; padding: 0px; margin: 0px;" src="{}"/>
                            <span style="font-size:20px; font-weight:bold;">{}</span>
                            </p>
                            </td>
                            </tr>
                            <tr style="background-color:gray; color:white; font-weight:bold;">
                        """.format(Color, len(Obj.Encabezados), URLImagenNotificacion, Obj.Titulo)
                        for Encabezado in Obj.Encabezados:
                            html += '<td style="width:auto;">{}</td>'.format(Encabezado)
                        html += """
                            </tr>
                        """
                        for Fila in Obj.Datos:
                            html += '<tr>'
                            for FilaMensaje in Fila:
                                html += '<td style="width:auto;">{}</td>'.format(FilaMensaje)
                            html += '</tr>'
                    else:
                        html += """
                            <div>
                            <table cellspacing="0" cellpadding="5" height="100%" width="100%" style="word-break:break-word">
                            <tbody style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:grey;text-align:left;word-break:break-word">
                            <tr style="background-color:{};color:white;font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-weight:bold;">
                            <td colspan="{}">
                            <p style="padding: 0px; margin: 0px;">
                            <img width="30px" height="30px" style="height:auto; padding: 0px; margin: 0px;" src="{}"/>
                            <span style="font-size:20px; font-weight:bold;">{}</span>
                            </p>
                            </td>
                            </tr>
                        """.format(Color, len(Obj.Encabezados), URLImagenNotificacion, Obj.Titulo)
                        for i in range(len(Obj.Encabezados)):
                            html += """
                                <tr>
                                <td width="auto" style="background-color:gray; color:white; font-weight:bold;">{}</td>
                            """.format(Obj.Encabezados[i])
                            for Fila in Obj.Datos:
                                mensaje = ''
                                if len(Fila) > i:
                                    mensaje = Fila[i]
                                html += '<td>{}</td>'.format(mensaje)
                            html += '</tr>'
            html += """
                </tbody>
                </table>
                </div>
                </td>
                </tr>
                </tbody>
                </table>
                </body>
                </html>
            """
            return html
        return ''
    except:
        GetExcept()
        return ''
