from backend.entidades import Metodo
from backend.logger import GetExcept
from backend.utils import FormatNotNull
from datetime import datetime
from datos.conexion import ConsultarSql, ObtenerConexion
from datos.entidad import Usuario, Usuario_V2, Empresa, Unidad, Linker
from threading import Lock, Timer


class Diccionarios():
    iniciado, lock = False, Lock()
    dictUsuario, dtUsuario = {}, datetime(2000, 1, 1)
    dictUsuario_V2, dtUsuario_V2 = {}, datetime(2000, 1, 1)
    dictEmpresas, dictLinkers, dictUnidades, dtEmpresas, dtLinkers, dtUnidades = {}, {},{}, datetime(2000, 1, 1), datetime(2000, 1, 1), datetime(2000, 1, 1)


    #region "---+ Memoria Perfiles +---"
    dictPerfiles={
        1:{"id": 1,"Empresa": "Innovalinks Admin", "Descripcion": "Tiene todos los permisos, autoriza altas y bajas"},
        2:{"id": 2,"Empresa": "Innovalinks", "Descripcion": "Tiene permiso de reiniciar"},
        3:{"id": 3,"Empresa": "Distribuidor", "Descripcion": "Solo puede ver informacion propia y resetear los endpoints que le corresponden"}}
    #endregion



    #region "---+ Memoria Usuario +---"

    @classmethod
    def CargarUsuario(cls):
        try:
            consulta = """
                SELECT 
                    int_id_usuario, int_id_perfil, int_id_distribuidor, var_nombre, var_apellidos, var_correo, var_usuario, bta_password, dt_fecha_registro, 
                    dt_fecha_modificado, bol_enuso 
                FROM cat.usuario
                WHERE {};
            """.format("dt_fecha_modificado > '{}'".format(cls.dtUsuario) if cls.iniciado else 'bol_enuso')
            grupoDeConexiones, datos = ObtenerConexion(Metodo.Memoria, 1, 1, 1)
            error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'CargarUsuario')
            if not error and afectados > 0:
                for fila in filas:
                    if fila['bol_enuso']:
                        usuario = Usuario_V2()
                        usuario.int_id = FormatNotNull('int', fila['int_id_usuario'])
                        usuario.int_idperfil = FormatNotNull('int', fila['int_id_perfil'])
                        usuario.int_iddistribuidor = FormatNotNull('int', fila['int_id_distribuidor'])
                        usuario.var_nombre = FormatNotNull('str', fila['var_nombre'])
                        usuario.var_apellidos = FormatNotNull('str', fila['var_apellidos'])
                        usuario.var_correo = FormatNotNull('str', fila['var_correo'])
                        usuario.var_usuario = FormatNotNull('str', fila['var_usuario'])
                        usuario.bta_password = FormatNotNull('str', fila['bta_password'])
                        usuario.dt_registro = FormatNotNull('dt', fila['dt_fecha_registro'])
                        usuario.dt_modificacion = FormatNotNull('dt', fila['dt_fecha_modificado'])
                        usuario.bol_enuso = FormatNotNull('bol', fila['bol_enuso'])
                        with cls.lock:
                            cls.dictUsuario[fila['int_id_usuario']] = usuario
                    else:
                        with cls.lock:
                            cls.dictUsuario.pop(fila['int_id_usuario'], None)
                    if fila['dt_fecha_modificado'] > cls.dtUsuario:
                        cls.dtUsuario = fila['dt_fecha_modificado']
        except:
            GetExcept(_Method=Metodo.Memoria)
    
    #endregion



    #region "---+ Memoria Usuario_V2 +---"

    @classmethod
    def CargarUsuario_V2(cls):
        try:
            consulta = """
                SELECT 
                    int_id, int_idperfil, int_iddistribuidor, var_nombre, var_apellidos, var_correo, var_usuario, bta_password, dt_registro, 
                    dt_modificacion, bol_enuso 
                FROM cat.usuario
                WHERE {};
            """.format("dt_modificacion > '{}'".format(cls.dtUsuario_V2) if cls.iniciado else 'bol_enuso')
            grupoDeConexiones, datos = ObtenerConexion(Metodo.Memoria, 2, 1, 1)
            error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'CargarUsuario_V2')
            if not error and afectados > 0:
                for fila in filas:
                    if fila['bol_enuso']:
                        usuario = Usuario_V2()
                        usuario.int_id = FormatNotNull('int', fila['int_id'])
                        usuario.int_idperfil = FormatNotNull('int', fila['int_idperfil'])
                        usuario.int_iddistribuidor = FormatNotNull('int', fila['int_iddistribuidor'])
                        usuario.var_nombre = FormatNotNull('str', fila['var_nombre'])
                        usuario.var_apellidos = FormatNotNull('str', fila['var_apellidos'])
                        usuario.var_correo = FormatNotNull('str', fila['var_correo'])
                        usuario.var_usuario = FormatNotNull('str', fila['var_usuario'])
                        usuario.bta_password = FormatNotNull('str', fila['bta_password'])
                        usuario.dt_registro = FormatNotNull('dt', fila['dt_registro'])
                        usuario.dt_modificacion = FormatNotNull('dt', fila['dt_modificacion'])
                        usuario.bol_enuso = FormatNotNull('bol', fila['bol_enuso'])
                        with cls.lock:
                            cls.dictUsuario_V2[fila['int_id']] = usuario
                    else:
                        with cls.lock:
                            cls.dictUsuario_V2.pop(fila['int_id'], None)
                    if fila['dt_modificacion'] > cls.dtUsuario_V2:
                        cls.dtUsuario_V2 = fila['dt_modificacion']
        except:
            GetExcept(_Method=Metodo.Memoria)
    
    #endregion


    #region "---+ Memoria Empresas +---"

    @classmethod
    def CargarEmpresas(cls):
        try:
            consulta = """
                SELECT int_id, var_nombre, bit_enuso, dt_fecha_modificacion, bit_activo, bit_distribuidor, int_iddistribuidor
                    FROM empresa.tblempresas
                WHERE {};
            """.format("dt_fecha_modificacion > '{}'".format(cls.dtEmpresas) if cls.iniciado else "bit_enuso = B'1'")
            grupoDeConexiones, datos = ObtenerConexion(Metodo.Memoria, 3, 1, 1)
            error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'CargarEmpresas')
            if not error and afectados > 0:
                for fila in filas:
                    if fila['bit_enuso']:
                        empresa= Empresa()
                        empresa.int_id = FormatNotNull('int', fila['int_id'])
                        empresa.int_iddistribuidor = FormatNotNull('int', fila['int_iddistribuidor'])
                        empresa.bit_enuso = FormatNotNull('bol', fila['bit_enuso'])
                        empresa.bit_activo = FormatNotNull('bol', fila['bit_activo'])
                        empresa.bit_distribuidor = FormatNotNull('bol', fila['bit_distribuidor'])
                        empresa.var_nombre = FormatNotNull('str', fila['var_nombre'])
                        empresa.dt_modificacion = FormatNotNull('dt', fila['dt_fecha_modificacion'])

                        with cls.lock:
                            cls.dictEmpresas[fila['int_id']] = empresa
                    else:
                        with cls.lock:
                            cls.dictEmpresas.pop(fila['int_id'], None)
                    if fila['dt_fecha_modificacion'] > cls.dtEmpresas:
                        cls.dtEmpresas = fila['dt_fecha_modificacion']
        except:
            GetExcept(_Method=Metodo.Memoria)
    
    #endregion


    #region "---+ Memoria Unidades +---"

    @classmethod
    def CargarUnidades(cls):
        try:
            consulta = """
                SELECT int_id, int_idlinker, int_idempresa, bit_enuso, var_nombre, var_placas, dt_fecha_modificacion
                    FROM unidad.tblunidad
                WHERE {};
            """.format("dt_fecha_modificacion > '{}'".format(cls.dtUnidades) if cls.iniciado else "bit_enuso = B'1'")
            grupoDeConexiones, datos = ObtenerConexion(Metodo.Memoria, 4, 1, 1)
            error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'CargarUnidades')
            if not error and afectados > 0:
                for fila in filas:
                    if fila['bit_enuso']:
                        unidad= Unidad()
                        unidad.int_id = FormatNotNull('int', fila['int_id'])
                        unidad.int_idlinker = FormatNotNull('int', fila['int_idlinker'])
                        unidad.int_idempresa = FormatNotNull('int', fila['int_idempresa'])
                        unidad.bit_enuso = FormatNotNull('bol', fila['bit_enuso'])
                        unidad.var_nombre = FormatNotNull('str', fila['var_nombre'])
                        unidad.var_placas = FormatNotNull('str', fila['var_placas'])
                        unidad.dt_modificacion = FormatNotNull('dt', fila['dt_fecha_modificacion'])

                        with cls.lock:
                            cls.dictUnidades[fila['int_id']] = unidad
                    else:
                        with cls.lock:
                            cls.dictUnidades.pop(fila['int_id'], None)
                    if fila['dt_fecha_modificacion'] > cls.dtUnidades:
                        cls.dtUnidades = fila['dt_fecha_modificacion']
        except:
            GetExcept(_Method=Metodo.Memoria)
    
    #endregion



    #region "---+ Memoria Linkers +---"

    @classmethod
    def CargarLinkers(cls):
        try:
            consulta = """
                SELECT int_id, int_idunidad, bit_enuso, var_numero_serie, var_linea1, var_ime, dt_fecha_modificacion, var_sim1
                    FROM linkers.tbllinker
                WHERE {};
            """.format("dt_fecha_modificacion > '{}'".format(cls.dtLinkers) if cls.iniciado else "bit_enuso = B'1'")
            grupoDeConexiones, datos = ObtenerConexion(Metodo.Memoria, 5, 1, 1)
            error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'CargarLinkers')
            if not error and afectados > 0:
                for fila in filas:
                    if fila['bit_enuso']:
                        linker= Linker()
                        linker.int_id = FormatNotNull('int', fila['int_id'])
                        linker.int_idunidad = FormatNotNull('int', fila['int_idunidad'])
                        linker.bit_enuso = FormatNotNull('bol', fila['bit_enuso'])
                        linker.var_numero_serie = FormatNotNull('str', fila['var_numero_serie'])
                        linker.var_linea1 = FormatNotNull('str', fila['var_linea1'])
                        linker.var_ime = FormatNotNull('str', fila['var_ime'])
                        linker.var_sim1 = FormatNotNull('str', fila['var_sim1'])
                        linker.dt_modificacion = FormatNotNull('dt', fila['dt_fecha_modificacion'])

                        with cls.lock:
                            cls.dictLinkers[fila['int_id']] = linker
                    else:
                        with cls.lock:
                            cls.dictLinkers.pop(fila['int_id'], None)
                    if fila['dt_fecha_modificacion'] > cls.dtLinkers:
                        cls.dtLinkers = fila['dt_fecha_modificacion']
        except:
            GetExcept(_Method=Metodo.Memoria)
    
    #endregion



def ActualizarMemoria() -> None:
    try:
        Diccionarios.CargarUsuario()
        Diccionarios.CargarUsuario_V2()
        Diccionarios.CargarLinkers()
        Diccionarios.CargarEmpresas()
        Diccionarios.CargarUnidades()

        if not Diccionarios.iniciado:
            Diccionarios.iniciado = True
    except:
        GetExcept(_Method=Metodo.Memoria)


def IniciarMemoria():
    try:
        ActualizarMemoria()
    except:
        GetExcept(_Method=Metodo.Memoria)
    finally:
        thread = Timer(1, IniciarMemoria)
        thread.name = 'Memoria'
        thread.start()