from datetime import datetime
from psycopg2.pool import PoolError, ThreadedConnectionPool

class Usuario:
    """
        Crea un objeto de tipo Usuario.
    """
    def __init__(self):
        """
            Inicializa un objeto Usuario.
        """
        self.int_id_usuario = 0
        self.int_id_perfil = 0
        self.int_id_distribuidor = 0
        self.var_nombre = ''
        self.var_apellidos = ''
        self.var_correo = ''
        self.var_usuario = ''
        self.bta_password = ''
        self.dt_fecha_registro: datetime = None
        self.dt_fecha_modificado: datetime = None
        self.bol_enuso = False

class Usuario_V2:
    """
        Crea un objeto de tipo Usuario.
    """
    def __init__(self):
        """
            Inicializa un objeto Usuario_V2.
        """
        self.int_id = 0
        self.int_idperfil = 0
        self.int_iddistribuidor = 0
        self.var_nombre = ''
        self.var_apellidos = ''
        self.var_correo = ''
        self.var_usuario = ''
        self.bta_password = ''
        self.dt_registro: datetime = None
        self.dt_modificacion: datetime = None
        self.bol_enuso = False

class Empresa:
    """
        Crea un objeto de tipo Empresa.
    """
    def __init__(self):
        """
            Inicializa un objeto Empresa.
        """
        self.int_id = 0
        self.var_nombre = ''
        self.int_iddistribuidor = 0
        self.bit_activo = False
        self.bit_distribuidor = False
        self.bit_enuso = False
        self.dt_modificacion:datetime = None

class Linker:
    """
        Crea un objeto de tipo Linker.
    """
    def __init__(self):
        """
            Inicializa un objeto Linker.
        """
        self.int_id = 0
        self.int_idunidad = 0
        self.var_numero_serie = ''
        self.var_linea1 = ''
        self.var_ime = ''
        self.var_sim1 = ''
        self.bit_enuso = False
        self.dt_modificacion:datetime = None

class Unidad:
    """
        Crea un objeto de tipo Unidad.
    """
    def __init__(self):
        """
            Inicializa un objeto Unidad.
        """
        self.int_id = 0
        self.int_idlinker = 0
        self.int_idempresa = 0
        self.var_nombre = ''
        self.var_placas = ''
        self.bit_enuso = False
        self.dt_modificacion:datetime = None


