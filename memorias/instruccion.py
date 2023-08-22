from psycopg2.pool import PoolError, ThreadedConnectionPool
from backend.entidades import Metodo
from backend.logger import GetExcept, LogErrores
from datos.conexion import ConsultarSql, EjecutarSql, ObtenerConexion, EscribirLogSql, IniciarConexion, EjecutarConsultaSql
from utilidades.seguridad import encryptPsw
from random import choice, shuffle
from datetime import datetime




#region "---+ Modificar Usuario +---"
def ModificarUsuario(_IdUsuario: int, _IdUsuarioCat: int, _Perfil: int, _Distribuidor: int, _Nombre: str, _Apellidos: str, _Correo: str, _Usuario: str, _Contrasena: str) -> bool:
    resultado = False
    try:
        _Distribuidor = 'null' if _Distribuidor == 0 else _Distribuidor
        consulta = """
            UPDATE cat.usuario SET int_id_perfil={}, int_id_distribuidor={}, var_nombre='{}', var_apellidos='{}', var_correo='{}', var_usuario='{}', bta_password={},  
            dt_fecha_modificado=Current_timestamp(3) AT TIME ZONE 'UTC' 
            WHERE int_id_usuario = {}
        """.format(int(_Perfil), _Distribuidor, str(_Nombre), str(_Apellidos), str(_Correo), str(_Usuario), str(encryptPsw(str(_Contrasena)))[1:], int(_IdUsuarioCat))
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 1, 4, 1)
        error, affect = EjecutarSql(datos, grupoDeConexiones, consulta, 'ModificarUsuario')
        if not error and affect > 0:
            resultado = True
    except:
        GetExcept()
    finally:
        return resultado 
#endregion

#region "---+ Borrar Usuario +---"
def BorrarUsuario(_IdUsuario: int, _IdUsuarioCat: int) -> bool:
    resultado = False
    try:
        consulta = """
            UPDATE cat.usuario
            SET bol_enuso=false, dt_fecha_modificado=Current_timestamp(3) AT TIME ZONE 'UTC'
            WHERE int_id_usuario={}
        """.format(_IdUsuarioCat)
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 1, 3, 2)
        error, afectados = EjecutarSql(datos, grupoDeConexiones, consulta, 'BorrarUsuario')
        if not error and afectados > 0:
            resultado = True
    except:
        GetExcept()
    finally:
        return resultado 
#endregion

#region "---+ Validar Eliminar Usuario +---"
def ValidarEliminarUsuario(_IdUsuarioCat: int) -> bool:
    valido = False
    try:
        consulta = """
            SELECT
                COUNT(*)
            FROM cat.usuario
            WHERE int_id_usuario = {} AND bol_enuso;
        """.format(_IdUsuarioCat)
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 1, 3, 1)
        error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'ValidarEliminarUsuario')
        if not error and afectados > 0:
            if filas[0]['count'] > 0:
                valido = True
    except:
        GetExcept()
    finally:
        return valido
#endregion  

#region "---+ Insertar Usuario +---"
def InsertarUsuario(_IdUsuario: int, _IdPerfil: int, _Distribuidor: int, _Nombre: str, _Apellidos: str, _Correo: str, _Usuario: str, _Contrasena: str) -> tuple:
    """
        Inserta un usuario para la plataforma de simglobal (emnify).
    """
    insertado, int_id = False, -1
    try:
        _Distribuidor = 'null' if _Distribuidor == 0 else _Distribuidor
        consulta = """
                INSERT INTO cat.usuario(
                    int_id_perfil, int_id_distribuidor, var_nombre, var_apellidos, var_correo,
                    var_usuario, bta_password, dt_fecha_registro, dt_fecha_modificado, bol_enuso)
                VALUES ({}, {}, '{}', '{}', '{}', '{}', {}, Current_timestamp(3) AT TIME ZONE 'UTC', Current_timestamp(3) AT TIME ZONE 'UTC', True) RETURNING int_id_usuario;
            """.format(int(_IdPerfil), _Distribuidor, str(_Nombre), str(_Apellidos), str(_Correo), str(_Usuario), str(encryptPsw(str(_Contrasena)))[1:])
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 1, 2, 2)
        error, afectados, filas = EjecutarConsultaSql(datos, grupoDeConexiones, consulta, 'InsertarUsuario')
        if not error and afectados > 0:
            insertado, int_id = True, filas[0]['int_id_usuario']
    except:
        GetExcept()
    finally:
        return insertado, int_id
#endregion

#region "---+ Validar Usuario +---"
def ValidarUsuario(_Usuario: str, _IdUsuarioCat: int = 0) -> tuple:
    valido, descuento = True, 0
    try:
        if _IdUsuarioCat > 0 :
            descuento = ValidarUsuarioId(_Usuario, _IdUsuarioCat)

        consulta = """
            SELECT COUNT(1) FROM cat.usuario WHERE TRIM(LOWER(var_usuario)) = '{}' AND bol_enuso;
        """.format(_Usuario.lower())
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 1, 2, 1)
        error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'ValidarUsuario')
        
        if not error and afectados + descuento > 0:
            if filas[0]['count'] > 0:
                valido = False
    except:
        GetExcept()
    finally:
        return valido 

def ValidarUsuarioId(_Usuario: str, _IdUsuarioCat: int):
    descuento = 0
    try:
        consulta = """
            SELECT var_usuario FROM cat.usuario WHERE int_id = {}
        """.format(_IdUsuarioCat)
        
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 1, 2, 1)
        error, afectados, filas = EjecutarConsultaSql(datos, grupoDeConexiones, consulta, 'ValidarUsuarioId')
            
        if not error and afectados == 1:
            if _Usuario == filas[0]['var_usuario']:
                descuento = -1
    except:
        GetExcept()
    finally:
        return descuento
#endregion




#region "---+ Modificar Usuario_V2 +---"
def ModificarUsuario_V2(_IdUsuario: int, _IdUsuarioCat: int, _Perfil: int, _Distribuidor: int, _Nombre: str, _Apellidos: str, _Correo: str, _Usuario: str, _Contrasena: str) -> bool:
    resultado = False
    try:
        _Distribuidor = 'null' if _Distribuidor == 0 else _Distribuidor
        consulta = """
                UPDATE cat.usuario SET int_id_perfil={}, int_id_distribuidor={}, var_nombre='{}', var_apellidos='{}', var_correo='{}', var_usuario='{}', bta_password={},  
                    dt_fecha_modificado=Current_timestamp(3) AT TIME ZONE 'UTC' 
                WHERE int_id_usuario = {} RETURNING int_id_usuario
            """.format(int(_Perfil), _Distribuidor, str(_Nombre), str(_Apellidos), str(_Correo), str(_Usuario), str(encryptPsw(str(_Contrasena)))[1:], int(_IdUsuarioCat))
        grupoDeConexion, dato = ObtenerConexion(Metodo.Proceso, 1, 4, 1)
        
        consulta2 = """
            UPDATE cat.usuario SET int_idperfil={}, int_iddistribuidor={}, var_nombre='{}', var_apellidos='{}', var_correo='{}', var_usuario='{}', bta_password={},  
                dt_modificacion=Current_timestamp(3) AT TIME ZONE 'UTC' 
            WHERE int_id = {} RETURNING int_id
        """.format(int(_Perfil), _Distribuidor, str(_Nombre), str(_Apellidos), str(_Correo), str(_Usuario), str(encryptPsw(str(_Contrasena)))[1:], int(_IdUsuarioCat))
        grupoDeConexion2, dato2 = ObtenerConexion(Metodo.Proceso, 2, 4, 1)
        datos = (dato, dato2)
        error, afectados, filas = TransaccionProcesoSql(datos, grupoDeConexion, grupoDeConexion2, consulta, consulta2, 'ModificarUsuario_V2')
        if not error and afectados > 0:
            if filas > 0:
                resultado = True
    except:
        GetExcept()
    finally:
        return resultado 
#endregion

#region "---+ Borrar Usuario_V2 +---"
def BorrarUsuario_V2(_IdUsuario: int, _IdUsuarioCat: int) -> bool:
    resultado = False
    try:
        consulta = """
            UPDATE cat.usuario
            SET bol_enuso=false, dt_fecha_modificado=Current_timestamp(3) AT TIME ZONE 'UTC'
            WHERE int_id_usuario={} RETURNING int_id_usuario
        """.format(_IdUsuarioCat)
        grupoDeConexion, dato = ObtenerConexion(Metodo.Proceso, 1, 3, 2)

        consulta2 = """
            UPDATE cat.usuario
            SET bol_enuso=false, dt_modificacion=Current_timestamp(3) AT TIME ZONE 'UTC'
            WHERE int_id={} RETURNING int_id
        """.format(_IdUsuarioCat)
        grupoDeConexiones2, dato2 = ObtenerConexion(Metodo.Proceso, 2, 3, 2)

        datos = (dato, dato2)
        error, afectados, filas = TransaccionProcesoSql(datos, grupoDeConexion, grupoDeConexiones2, consulta, consulta2, 'BorrarUsuario_V2')
        if not error and afectados > 0:
            if filas > 0:
                resultado = True
    except:
        GetExcept()
    finally:
        return resultado 
#endregion

#region "---+ Validar Eliminar Usuario_V2 +---"
def ValidarEliminarUsuario_V2(_IdUsuarioCat: int) -> bool:
    valido = False
    try:
        consulta = """
            SELECT
                COUNT(*)
            FROM cat.usuario
            WHERE int_id = {} AND bol_enuso;
        """.format(_IdUsuarioCat)
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 2, 3, 1)
        error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'ValidarEliminarUsuario_V2')
        if not error and afectados > 0:
            if filas[0]['count'] > 0:
                valido = True
    except:
        GetExcept()
    finally:
        return valido
#endregion

#region "---+ Insertar Usuario_V2 +---"
def InsertarUsuario_V2(_IdUsuario: int, _IdPerfil: int, _Distribuidor: int, _Nombre: str, _Apellidos: str, _Correo: str, _Usuario: str, _Contrasena: str) -> tuple:
    """
        Inserta un usuario para la plataforma de simglobal (emnify).
    """
    insertado, int_id = False, -1
    try:
        _Distribuidor = 'null' if _Distribuidor == 0 else _Distribuidor
        consulta = """
                INSERT INTO cat.usuario(
                    int_idperfil, int_iddistribuidor, var_nombre, var_apellidos, var_correo,
                    var_usuario, bta_password, dt_registro, dt_modificacion, bol_enuso)
                VALUES ({}, {}, '{}', '{}', '{}', '{}', {}, Current_timestamp(3) AT TIME ZONE 'UTC', Current_timestamp(3) AT TIME ZONE 'UTC', True) RETURNING int_id;
            """.format(int(_IdPerfil), _Distribuidor, str(_Nombre), str(_Apellidos), str(_Correo), str(_Usuario), str(encryptPsw(str(_Contrasena)))[1:])
        grupoDeConexion, dato = ObtenerConexion(Metodo.Proceso, 2, 2, 2)

        consulta2 = """
                INSERT INTO cat.usuario(
                    int_id_perfil, int_id_distribuidor, var_nombre, var_apellidos, var_correo,
                    var_usuario, bta_password, dt_fecha_registro, dt_fecha_modificado, bol_enuso)
                VALUES ({}, {}, '{}', '{}', '{}', '{}', {}, Current_timestamp(3) AT TIME ZONE 'UTC', Current_timestamp(3) AT TIME ZONE 'UTC', True) RETURNING int_id_usuario;
            """.format(int(_IdPerfil), _Distribuidor, str(_Nombre), str(_Apellidos), str(_Correo), str(_Usuario), str(encryptPsw(str(_Contrasena)))[1:])
        grupoDeConexion2, dato2 = ObtenerConexion(Metodo.Proceso, 1, 2, 2)

        datos = (dato, dato2)
        error, afectados, filas = TransaccionProcesoSql(datos, grupoDeConexion, grupoDeConexion2, consulta, consulta2, 'InsertarUsuario_V2')
        
        if not error and afectados > 0:
            insertado, int_id = True, filas
    except:
        GetExcept()
    finally:
        return insertado, int_id
#endregion

#region "---+ Validar Insertar Usuario_V2 +---"

def ValidarUsuario_V2(_Usuario: str, _IdUsuarioCat: int = 0) -> tuple:
    valido, descuento = True, 0
    try:
        if _IdUsuarioCat > 0 :
            descuento = ValidarUsuarioId_V2(_Usuario, _IdUsuarioCat)

        consulta = """
            SELECT COUNT(1) FROM cat.usuario WHERE TRIM(LOWER(var_usuario)) = '{}' AND bol_enuso;
        """.format(_Usuario.lower())
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 2, 2, 1)
        error, afectados, filas = ConsultarSql(datos, grupoDeConexiones, consulta, 'ValidarUsuario_V2')
        
        if not error and afectados + descuento > 0:
            if filas[0]['count'] > 0:
                valido = False
    except:
        GetExcept()
    finally:
        return valido 

def ValidarUsuarioId_V2(_Usuario: str, _IdUsuarioCat: int):
    descuento = 0
    try:
        consulta = """
            SELECT var_usuario FROM cat.usuario WHERE int_id = {}
        """.format(_IdUsuarioCat)
        
        grupoDeConexiones, datos = ObtenerConexion(Metodo.Proceso, 2, 2, 1)
        error, afectados, filas = EjecutarConsultaSql(datos, grupoDeConexiones, consulta, 'ValidarUsuarioId_V2')
            
        if not error and afectados == 1:
            if _Usuario == filas[0]['var_usuario']:
                descuento = -1
    except:
        GetExcept()
    finally:
        return descuento
#endregion




#region "---+ Ejecutar SQL  +---"

def TransaccionProcesoSql(_Datos: tuple, _GrupoDeConexion: ThreadedConnectionPool, _GrupoDeConexion2: ThreadedConnectionPool, _Query: str, _Query2: str, _Metodo='') -> bool:
    """
        Ejecuta varias instrucciones sql y solo si todas se llevan
        a cabo sin ningun problema se realiza un commit y retorna
        un true en caso contrario se realiza un rollback y retorna
        un false.
    """
    global contadorErroresEnGrupo, limiteErroresEnGrupo
    afectados, filas = 0, 0
    Consultas, error, bandera = True, False, None
    try:
        conexion = _GrupoDeConexion.getconn()
        cursor = conexion.cursor()
        conexion2 = _GrupoDeConexion2.getconn()
        cursor2 = conexion2.cursor()
        try:
            cursor.execute(_Query)
            cursor2.execute(_Query2)
            if cursor.rowcount < 0 or cursor2.rowcount < 0:
                bandera = True
            else:
                afectados = cursor.rowcount + cursor2.rowcount
            id = cursor.fetchone()[0]
            id2 = cursor2.fetchone()[0]
            if id == id2:
                filas = id
            else:
                bandera = True
            if bandera:
                conexion.rollback()
                conexion2.rollback()
                filas = 0
            else:
                conexion.commit()
                conexion2.commit()
                error = False
                Consultas = (_Query, _Query2)
        except Exception as e:
            conexion.rollback()
            conexion2.rollback()
            filas = 0
            for query in Consultas:
                LogErrores('connection', 'TransactionSql', datetime.utcnow(), _Metodo, str(e), _Consulta=query)
            logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), str(_Datos), str(e).replace('/n', ' ')), '--:SQL:'.join(Consultas))
            GetExcept(_Message=_Metodo, _Link=logSql)
        cursor.close()
        cursor2.close()
        _GrupoDeConexion.putconn(conexion)
        _GrupoDeConexion2.putconn(conexion2)
    except PoolError as pe:
        if str(pe) == 'connection pool exhausted':
            contadorErroresEnGrupo += 1
            if contadorErroresEnGrupo >= limiteErroresEnGrupo:
                IniciarConexion()
        logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), str(_Datos), str(pe).replace('/n', ' ')), '--:SQL:'.join(Consultas))
        GetExcept(_Message=_Metodo, _Link=logSql)
    except Exception as e:
        logSql = EscribirLogSql(_Metodo, '{}|{}/n--{}/n'.format(datetime.utcnow(), str(_Datos), str(e).replace('/n', ' ')), '--:SQL:'.join(Consultas))
        GetExcept(_Message=_Metodo, _Link=logSql)
    finally:
        return error, afectados, filas

#endregion