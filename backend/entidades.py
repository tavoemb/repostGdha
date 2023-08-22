from enum import Enum


class Empresa(Enum):
    """
        Enumerador para las variables de Empresa.
    """
    NoConfigurado = 0
    Elevenminds = 1
    GlobalTrack = 2
    Innovalinks = 3
    SisTechnologies = 4
    TheRightConnectionsDeMexico = 5


class Ambiente(Enum):
    """
        Enumerador para las variables de ambiente.
    """
    TRCMPruebas = -501
    NaanixPruebas = -401
    LinkerWebRespaldoPruebas = -302
    LinkerWebPruebas = -301
    SpheregtC5NLPruebas = -210
    EtrackingPruebas = -209
    SpheregtValuePruebas = -208
    SpheregtFiscaliaPruebas = -207
    BigDataTMLaEuropeaPruebas = -206
    BigDataTMSigmaPruebas = -205
    SpheregtC4SanPedroPruebas = -204
    CoSoAVLPruebas = -203
    SpheregtPruebas = -202
    BigDataTMPruebas = -201
    ElevenPruebas = -101
    NoConfigurado = 0
    Elevenminds = 101
    BigDataTM = 201
    Spheregt = 202
    CoSoAVL = 203
    SpheregtC4SanPedro = 204
    BigDataTMSigma = 205
    BigDataTMLaEuropea = 206
    SpheregtFiscalia = 207
    SpheregtValue = 208
    Etracking = 209
    SpheregtC5NL = 210
    LinkerWeb = 301
    LinkerWebRespaldo = 302
    Naanix = 401
    TRCM = 501


class Telegram(Enum):
    """
        Enumerador para las variables del tipo de envio de telegram empleado.
    """
    # Servicios = 1
    Alertas = 2
    Errores = 3
    Monitoreo = 4
    Advertencias = 100
    Especifico = 1000


class Servicio(Enum):
    """
        Enumerador para las variables del tipo de servicio empleado.
    """
    Servicio = 1
    Web = 2


class Metodo(Enum):
    """
        Enumerador para las variables del tipo de metodo empleado.
    """
    Memoria = 0
    Proceso = 1
    Rest = 2
    WebSocket = 3
    TeleBot = 4
    Udp = 5


class Dominio(Enum):
    """
        Enumerador para las variables del tipo de dominio.
    """
    backend = 0
    plataforma = 1
    movil = 2
    admin = 3
    externos = 4
    monitor = 5
    plataformaCloud = 6
    movilCloud = 7
    adminCloud = 8
    externosCloud = 9
    monitorCloud = 10
    backendCloud = 11


class Evento(Enum):
    """
        Enumerador para las variables del tipo de evento obtenido.
    """
    Alerta = 0
    Informativo = 1
    Error = 2
    Critico = 3


class Correo(Enum):
    """
        Enumerador para las variables del tipo de correo.
    """
    Normal = 0
    Error = 1
    Prioritario = 2


class MimeType(Enum):
    """
        Enumerador para las variables del tipo de contenido de un correo y telegram.
    """
    Plain = 0
    Html = 1
    Markdown = 2
    MarkdownV2 = 3


class Orientacion(Enum):
    """
        Orientacion para enviar un correo.
    """
    Vertical = 1
    Horizontal = 2


class EnvioCorreo(Enum):
    """
        Tipo de envio de un correo, este tipo define el color.
    """
    Precaucion = 1
    Error = 2
    Notificacion = 3
    Ok = 4
    Reporte = 5
    Recordatorio = 6
    Resumen = 7


class Cola:
    """
        Estructura de datos de un objeto tipo Cola.
    """
    def __init__(self):
        """
            Inicializa el objeto de tipo Cola.
        """
        self.items = []

    def empty(self) -> bool:
        """
            Retorna un booleano que indica si el objeto esta vacio.
        """
        return self.items == []

    def add(self, item) -> None:
        """
            Agrega un item al objeto en primera posicion.
        """
        self.items.insert(0, item)

    def remove(self) -> int:
        """
            Elimina el ultimo item y retorna el index de este.
        """
        return self.items.pop()

    def size(self) -> int:
        """
            Retorna la longitud del objeto.
        """
        return len(self.items)

    def get(self) -> list:
        """
            Retorna el objeto list con los items.
        """
        return self.items


class Mensaje:
    """
        Estructura de datos de un objeto tipo Mensaje para correo.
    """
    def __init__(self):
        """
            Inicializa el objeto de tipo Mensaje.
        """
        self.De = ''
        self.Para = []
        self.Datos = ''


class Tabla:
    """
    Estructura de datos de un objeto tipo Tabla para un correo html.
    """
    def __init__(self, Titulo: str, Mensaje: str, Encabezados: list, Datos: list, Orientacion: Orientacion, TipoNotificacion: EnvioCorreo):
        """
            Inicializa un objeto de tipo Tabla.
        """
        self.Titulo = Titulo
        self.Mensaje = Mensaje
        self.Encabezados = Encabezados
        self.Datos = Datos
        self.Orientacion = Orientacion
        self.TipoNotificacion = TipoNotificacion


class Aplicacion:
    """
        Estructura de datos de tipo Aplicacion para el servicio.
    """
    def __init__(self):
        """
            Inicializa un objeto de tipo Aplicacion.
        """
        self.IdServicio = 0
        self.IdInstalacion = 0
        self.IdInicio = 0
        self.NombreEquipo = ''
        self.IPEquipo = ''
        self.Empresa: Empresa = Empresa.NoConfigurado
        self.Ambiente: Ambiente = Ambiente.NoConfigurado
        self.NombreServicio = ''
        self.Descripcion = ''
        self.InicioDinamico = False
        self.TipoServicio = 0
        self.DireccionURL = ''
        self.DireccionLogo = ''
        self.DirectorioLogServicio = ''
        self.DirectorioAlerta = ''
        self.DirectorioArchivo = ''
        self.DirectorioPlantilla = ''
        self.DirectorioSql = ''
        self.Dominio = ''
        self.DominioCloud = False
        self.CorreoSoporte = ''
        self.CorreoErrores = ''
        self.CorreoDominioError = ''
        self.CorreoDominioServicio = ''
        self.CorreoQueEnviaServicio = ''
        self.CorreoQueEnviaErrores = ''
        self.DestinatariosUrgentes = ''
        self.EsConsola = False
        self.EnviaTelegram = False
        self.EnviaCorreo = False
        self.Destinatarios = []
        self.DestinatariosCopia = []
        self.DestinatariosCopiaOculta = []
        self.Version = "20000101.0"
        self.NombreCorreo = ''
        self.HTTP = {'Ip': '', 'Puerto': 0}
        self.WS = {'Ip': '', 'Puerto': 0}
        self.UDP = {'Ip': '', 'PuertoEscucha': 0, 'PuertoEnvia': 0}
        self.ServidoresBD = {}
        self.FuncionesBD = {}
        self.ServidoresSMTP = []
        self.Log = False
        self.LogMemoria = False
        self.DirectorioLog = ''
        self.DirectorioArc = ''
        self.Variables = {}
