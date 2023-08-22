from backend.entidades import Metodo
from backend.logger import GetExcept
from backend.utils import FormatNotNone
from datetime import datetime
from memorias import instruccion
from memorias.memoria import Diccionarios as memoriaGeneral
from random import choice
from utilidades.seguridad import DecryptPsw


#region "---+ Función Perfil +---"

def ObtenerPerfil(_Metodo: Metodo) -> list:
    datos, resultado = [], -1
    try:
        datos = list(memoriaGeneral.dictPerfiles.values())
        resultado = 1
    except:
        GetExcept(_Method=_Metodo)
        resultado = -2
    finally:
        return datos, resultado

#endregion

#region "---+ Funciones Usuario +---"

def EditarUsuario(_Metodo: Metodo, _IdUsuario: int, _IdUsuarioCat: int, _Perfil: int, _Distribuidor: int, _Nombre: str, _Apellidos: str, _Correo: str, _Usuario: str, _Contrasena: str) -> list:
    resultado = -1
    try:
        valido = instruccion.ValidarUsuario(_Usuario, _IdUsuarioCat)
        resultado = -3
        if valido:
            resultado = -4
            if _Perfil in memoriaGeneral.dictPerfiles:
                if _Perfil != 1:
                    resultado = -5
                    if _Perfil == 3 and not _Distribuidor:
                        resultado = -6
                    else:
                        actualizado= instruccion.ModificarUsuario(_IdUsuario, _IdUsuarioCat, _Perfil, _Distribuidor, _Nombre, _Apellidos, _Correo, _Usuario, _Contrasena)
                        resultado = _IdUsuarioCat if actualizado else -6
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return resultado


def EliminarUsuario(_Metodo: Metodo, _IdUsuario: int, _IdUsuarioCat: int) -> int:
    resultado = -1
    try:
        valido = instruccion.ValidarEliminarUsuario(_IdUsuarioCat)
        resultado = -3
        if valido:
            eliminado = instruccion.BorrarUsuario(_IdUsuario, _IdUsuarioCat)
            resultado = _IdUsuarioCat if eliminado else -3
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return resultado


def NuevoUsuario(_Metodo: Metodo, _IdUsuario: int, _Perfil: int, _Distribuidor: int, _Nombre: str, _Apellidos: str, _Correo: str, _Usuario: str, _Contrasena: str) -> list:
    resultado =  -1
    try:
        valido = instruccion.ValidarUsuario(_Usuario)
        resultado = -3
        if valido:
            resultado = -4
            if _Perfil in memoriaGeneral.dictPerfiles:
                if _Perfil != 1:
                    resultado = -5
                    if _Perfil == 3 and not _Distribuidor:
                        resultado = -6
                    else:
                        insertado, int_id= instruccion.InsertarUsuario(_IdUsuario, _Perfil, _Distribuidor, _Nombre, _Apellidos, _Correo, _Usuario, _Contrasena)
                        print('Usuario:', int_id, _Usuario)
                        resultado = int_id if insertado else -6
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return resultado


def ObtenerUsuario(_Metodo: Metodo, _Mofificacion: datetime) -> list:
    datos, resultado = [], -1
    try:
        _Mofificacion = datetime(2000, 1, 1) if _Mofificacion is None else _Mofificacion
        datos = [
            {
                'IdUsuario': FormatNotNone('int', usuario.int_id),
                'IdPerfil': FormatNotNone('int', usuario.int_idperfil),
                'IdDistribuidor': FormatNotNone('int', usuario.int_iddistribuidor),
                'Nombre': FormatNotNone('str', usuario.var_nombre),
                'Apellidos': FormatNotNone('str', usuario.var_apellidos),
                'Correo': FormatNotNone('str', usuario.var_correo),
                'Usuario': FormatNotNone('str', usuario.var_usuario),
                'Password': FormatNotNone('str', DecryptPsw(usuario.bta_password)),
                'Registro': FormatNotNone('dt', usuario.dt_registro),
                'Modificacion': FormatNotNone('dt', usuario.dt_modificacion),
                'EnUso': FormatNotNone('bol', usuario.bol_enuso),
            }
            for usuario in tuple(memoriaGeneral.dictUsuario.values())
            if usuario.dt_modificacion > _Mofificacion
        ]
        resultado = 1
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return datos, resultado

#endregion


#region "---+ Funciones Usuario V2 +---"

def EditarUsuario_V2(_Metodo: Metodo, _IdUsuario: int, _IdUsuarioCat: int, _Perfil: int, _Distribuidor: int, _Nombre: str, _Apellidos: str, _Correo: str, _Usuario: str, _Contrasena: str) -> list:
    resultado = -1
    try:
        valido = instruccion.ValidarUsuario_V2(_Usuario, _IdUsuarioCat)
        resultado = -3
        if valido:
            resultado = -4
            if _Perfil in memoriaGeneral.dictPerfiles:
                if _Perfil != 1:
                    resultado = -5
                    if _Perfil == 3 and not _Distribuidor:
                        resultado = -6
                    else:
                        actualizado= instruccion.ModificarUsuario_V2(_IdUsuario, _IdUsuarioCat, _Perfil, _Distribuidor, _Nombre, _Apellidos, _Correo, _Usuario, _Contrasena)
                        resultado = _IdUsuarioCat if actualizado else -6
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return resultado


def EliminarUsuario_V2(_Metodo: Metodo, _IdUsuario: int, _IdUsuarioCat: int) -> int:
    resultado = -1
    try:
        valido = instruccion.ValidarEliminarUsuario_V2(_IdUsuarioCat)
        resultado = -3
        if valido:
            eliminado = instruccion.BorrarUsuario_V2(_IdUsuario, _IdUsuarioCat)
            resultado = _IdUsuarioCat if eliminado else -3
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return resultado


def NuevoUsuario_V2(_Metodo: Metodo, _IdUsuario: int, _Perfil: int, _Distribuidor: int, _Nombre: str, _Apellidos: str, _Correo: str, _Usuario: str, _Contrasena: str) -> list:
    resultado =  -1
    try:
        valido = instruccion.ValidarUsuario_V2(_Usuario)
        resultado = -3
        if valido:
            resultado = -4
            if _Perfil in memoriaGeneral.dictPerfiles:
                if _Perfil != 1:
                    resultado = -5
                    if _Perfil == 3 and not _Distribuidor:
                        resultado = -6
                    else:
                        insertado, int_id= instruccion.InsertarUsuario_V2(_IdUsuario, _Perfil, _Distribuidor, _Nombre, _Apellidos, _Correo, _Usuario, _Contrasena)
                        print('Usuario:', int_id, _Usuario)
                        resultado = int_id if insertado else -6
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return resultado


def ObtenerUsuario_V2(_Metodo: Metodo, _Modificacion: datetime, _Version: int) -> list:
    datos, resultado = [], -1
    try:
        if _Version in (1, 2):
            if _Version == 1:
                dict = memoriaGeneral.dictUsuario.values()
            if _Version == 2:
                dict = memoriaGeneral.dictUsuario_V2.values()
            _Modificacion = datetime(2000, 1, 1) if _Modificacion is None else _Modificacion
            datos = [
                {
                    'IdUsuario': FormatNotNone('int', usuario.int_id),
                    'IdPerfil': FormatNotNone('int', usuario.int_idperfil),
                    'IdDistribuidor': FormatNotNone('int', usuario.int_iddistribuidor),
                    'Nombre': FormatNotNone('str', usuario.var_nombre),
                    'Apellidos': FormatNotNone('str', usuario.var_apellidos),
                    'Correo': FormatNotNone('str', usuario.var_correo),
                    'Usuario': FormatNotNone('str', usuario.var_usuario),
                    'Password': FormatNotNone('str', DecryptPsw(usuario.bta_password)),
                    'Registro': FormatNotNone('dt', usuario.dt_registro),
                    'Modificacion': FormatNotNone('dt', usuario.dt_modificacion),
                    'EnUso': FormatNotNone('bol', usuario.bol_enuso),
                }
                for usuario in tuple(dict) 
                
                if usuario.dt_modificacion > _Modificacion
            ]
            resultado = 1
        else:
            datos = 'Elija una versión entre 1-2'
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return datos, resultado

#endregion


#region "---+ Funciones Empresas +---"

def ObtenerEmpresas(_Metodo: Metodo, _Mofificacion: datetime) -> list:
    datos, resultado = [], -1
    try:
        _Mofificacion = datetime(2000, 1, 1) if _Mofificacion is None else _Mofificacion
        datos = [
            {
                'IdEmpresa': FormatNotNone('int', empresa.int_id),
                'Nombre': FormatNotNone('str', empresa.var_nombre),
                'Modificacion': FormatNotNone('dt', empresa.dt_modificacion),
                'Activo': FormatNotNone('bol', empresa.bit_activo),
                'Distribuidor': FormatNotNone('bol', empresa.bit_distribuidor),
                'IdDistribuidor': FormatNotNone('int', empresa.int_iddistribuidor),
                'Enuso': FormatNotNone('bol', empresa.bit_enuso ),
            }
            for empresa in tuple(memoriaGeneral.dictEmpresas.values())
            if empresa.dt_modificacion > _Mofificacion
        ]
        resultado = 1
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return datos, resultado
    
#endregion

#region "---+ Funciones Linkers +---"

def ObtenerLinkers(_Metodo: Metodo, _Mofificacion: datetime) -> list:
    datos, resultado= [], -1
    try:
        _Mofificacion = datetime(2000, 1, 1) if _Mofificacion is None else _Mofificacion
        datos = [
            {
                'IdLinker': FormatNotNone('int', linker.int_id),
                'IdUnidad': FormatNotNone('int', linker.int_idunidad),
                'NumeroSerie': FormatNotNone('str', linker.var_numero_serie),
                'Linea1': FormatNotNone('str', linker.var_linea1),
                'Ime': FormatNotNone('str', linker.var_ime ),
                'Sim1': FormatNotNone('str', linker.var_sim1),
                'EnUso': FormatNotNone('bol', linker.bit_enuso),
                'Modificacion': FormatNotNone('dt', linker.dt_modificacion),
            }
            for linker in tuple(memoriaGeneral.dictLinkers.values())
            if linker.dt_modificacion > _Mofificacion
        ]
        resultado = 1
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return datos, resultado
    
#endregion

#region "---+ Funciones Unidades +---"

def ObtenerUnidades(_Metodo: Metodo, _Mofificacion: datetime) -> list:
    datos, resultado= [], -1
    try:
        _Mofificacion = datetime(2000, 1, 1) if _Mofificacion is None else _Mofificacion
        datos = [
            {
                'IdUnidad': FormatNotNone('int', unidad.int_id),
                'IdLinker': FormatNotNone('int', unidad.int_idlinker),
                'IdEmpresa': FormatNotNone('int', unidad.int_idempresa),
                'Nombre': FormatNotNone('str', unidad.var_nombre),
                'Placas': FormatNotNone('str', unidad.var_placas),
                'EnUso': FormatNotNone('bol', unidad.bit_enuso),
                'Modificacion': FormatNotNone('dt', unidad.dt_modificacion),
            }
            for unidad in tuple(memoriaGeneral.dictUnidades.values())
            if unidad.dt_modificacion > _Mofificacion
        ]
        resultado = 1
    except:
        resultado = -2
        GetExcept(_Method=_Metodo)
    finally:
        return datos, resultado
    
#endregion

