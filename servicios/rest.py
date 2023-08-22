from backend.configuracion import appConfig
from backend.entidades import Metodo
from backend.logger import GetExcept
from backend.seguridad import ValidarToken
from backend.utils import ValidarParametros
from flask import Flask, request
from flask_compress import Compress
from flask_cors import CORS
from flask_restful import Api, Resource
from servicios import funcion
from threading import Thread

class Version_ObtenerVersion(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos = {
                '{}_{}_{}'.format(appConfig.IdServicio, appConfig.IdInstalacion, appConfig.NombreServicio): appConfig.Version,
                appConfig.NombreEquipo: '{}:{}'.format(appConfig.HTTP['Ip'], appConfig.HTTP['Puerto']),
            }
            resultado = 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}


#region "---+ Rest Perfil +---"

class Catalogo_ObtenerPerfil(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.ObtenerPerfil.__name__,
                'Informacion': 'Obtiene una lista de los perfiles existentes.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}
        
    def post(self):
        datos, mensaje, resultado = [], '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'Modificacion': {'type': 'dt', 'required': False}
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            datos, resultado = funcion.ObtenerPerfil(Metodo.Rest)
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Mensaje': mensaje, 'Resultado': resultado}

#endregion

#region "---+ Rest Usuario +---"

class Catalogo_EditarUsuario(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.EditarUsuario.__name__,
                'Informacion': 'Editar un usuario existente.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}

    def post(self):
        mensaje, resultado = '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'IdUsuarioCat': {'type': 'int', 'required': True},
                'Perfil': {'type': 'int', 'required': True},
                'Distribuidor': {'type': 'int', 'required': True},
                'Nombre': {'type': 'str', 'required': True},
                'Apellidos': {'type': 'str', 'required': True},
                'Correo': {'type': 'str', 'required': True},
                'Usuario': {'type': 'str', 'required': True},
                'Contrasena': {'type': 'str', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            resultado = funcion.EditarUsuario(Metodo.Rest, dPV['IdUsuario'], dPV['IdUsuarioCat'], dPV['Perfil'], dPV['Distribuidor'], dPV['Nombre'], dPV['Apellidos'], dPV['Correo'], dPV['Usuario'], dPV['Contrasena'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Mensaje': mensaje, 'Resultado': resultado}


class Catalogo_EliminarUsuario(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.EliminarUsuario.__name__,
                'Informacion': 'Elimina un usuario.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}

    def post(self):
        mensaje, resultado = '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'IdUsuarioCat': {'type': 'int', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            #if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            resultado = funcion.EliminarUsuario(Metodo.Rest,dPV['IdUsuario'], dPV['IdUsuarioCat'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Mensaje': mensaje, 'Resultado': resultado}


class Catalogo_NuevoUsuario(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.NuevoUsuario.__name__,
                'Informacion': 'Inserta un nuevo usuario.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}

    def post(self):
        mensaje, resultado = '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'Perfil': {'type': 'int', 'required': True},
                'Distribuidor': {'type': 'int', 'required': True},
                'Nombre': {'type': 'str', 'required': True},
                'Apellidos': {'type': 'str', 'required': True},
                'Correo': {'type': 'str', 'required': True},
                'Usuario': {'type': 'str', 'required': True},
                'Contrasena': {'type': 'str', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            resultado = funcion.NuevoUsuario(Metodo.Rest, dPV['IdUsuario'], dPV['Perfil'], dPV['Distribuidor'], dPV['Nombre'], dPV['Apellidos'], dPV['Correo'], dPV['Usuario'], dPV['Contrasena'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Mensaje': mensaje, 'Resultado': resultado}


class Catalogo_ObtenerUsuario(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.ObtenerUsuario.__name__,
                'Informacion': 'Obtiene una lista de los usuarios.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}
        
    def post(self):
        datos, mensaje, resultado = [], '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'Modificacion': {'type': 'dt', 'required': False}
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            datos, resultado = funcion.ObtenerUsuario(Metodo.Rest, dPV['Modificacion'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Mensaje': mensaje, 'Resultado': resultado}

#endregion

#region "---+ Rest Usuario_V2 +---"

class Catalogo_EditarUsuario_V2(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.EditarUsuario_V2.__name__,
                'Informacion': 'Editar un usuario existente.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}

    def post(self):
        mensaje, resultado = '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'IdUsuarioCat': {'type': 'int', 'required': True},
                'Perfil': {'type': 'int', 'required': True},
                'Distribuidor': {'type': 'int', 'required': True},
                'Nombre': {'type': 'str', 'required': True},
                'Apellidos': {'type': 'str', 'required': True},
                'Correo': {'type': 'str', 'required': True},
                'Usuario': {'type': 'str', 'required': True},
                'Contrasena': {'type': 'str', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            resultado = funcion.EditarUsuario_V2(Metodo.Rest, dPV['IdUsuario'], dPV['IdUsuarioCat'], dPV['Perfil'], dPV['Distribuidor'], dPV['Nombre'], dPV['Apellidos'], dPV['Correo'], dPV['Usuario'], dPV['Contrasena'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Mensaje': mensaje, 'Resultado': resultado}


class Catalogo_EliminarUsuario_V2(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.EliminarUsuario_V2.__name__,
                'Informacion': 'Elimina un usuario.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}

    def post(self):
        mensaje, resultado = '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'IdUsuarioCat': {'type': 'int', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            #if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            resultado = funcion.EliminarUsuario_V2(Metodo.Rest,dPV['IdUsuario'], dPV['IdUsuarioCat'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Mensaje': mensaje, 'Resultado': resultado}


class Catalogo_NuevoUsuario_V2(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.NuevoUsuario_V2.__name__,
                'Informacion': 'Inserta un nuevo usuario.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}

    def post(self):
        mensaje, resultado = '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'Perfil': {'type': 'int', 'required': True},
                'Distribuidor': {'type': 'int', 'required': True},
                'Nombre': {'type': 'str', 'required': True},
                'Apellidos': {'type': 'str', 'required': True},
                'Correo': {'type': 'str', 'required': True},
                'Usuario': {'type': 'str', 'required': True},
                'Contrasena': {'type': 'str', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            resultado = funcion.NuevoUsuario_V2(Metodo.Rest, dPV['IdUsuario'], dPV['Perfil'], dPV['Distribuidor'], dPV['Nombre'], dPV['Apellidos'], dPV['Correo'], dPV['Usuario'], dPV['Contrasena'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Mensaje': mensaje, 'Resultado': resultado}


class Catalogo_ObtenerUsuario_V2(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.ObtenerUsuario_V2.__name__,
                'Informacion': 'Obtiene una lista de los usuarios.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}
        
    def post(self):
        datos, mensaje, resultado = [], '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'Modificacion': {'type': 'dt', 'required': False},
                'Version': {'type': 'int', 'required': True},

            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            datos, resultado = funcion.ObtenerUsuario_V2(Metodo.Rest, dPV['Modificacion'], dPV['Version'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Mensaje': mensaje, 'Resultado': resultado}

#endregion


#region "---+ Rest Obtener Empresas +---"
class Empresa_ObtenerEmpresas(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.ObtenerEmpresas.__name__,
                'Informacion': 'Obtiene una lista de empresas.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}
        
    def post(self):
        datos, mensaje, resultado = [], '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'Modificacion': {'type': 'dt', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            datos, resultado = funcion.ObtenerEmpresas(Metodo.Rest, dPV['Modificacion'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Mensaje': mensaje, 'Resultado': resultado}
#endregion



#region "---+ Rest Obtener Linkers +---"
class Linker_ObtenerLinkers(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.ObtenerLinkers.__name__,
                'Informacion': 'Obtiene una lista de linkers.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}
        
    def post(self):
        datos, mensaje, resultado = [], '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'Modificacion': {'type': 'dt', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            datos, resultado = funcion.ObtenerLinkers(Metodo.Rest, dPV['Modificacion'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Mensaje': mensaje, 'Resultado': resultado}
#endregion



#region "---+ Rest Obtener Unidades +---"
class Unidad_ObtenerUnidades(Resource):
    def get(self):
        datos, resultado = {}, -1001
        try:
            datos, resultado = {
                'Mensaje': funcion.ObtenerUnidades.__name__,
                'Informacion': 'Obtiene una lista de unidades.',
                'Respuesta 1': 'Ok.',
                'Respuesta -1': 'Error: En metodo de proceso.',
                'Respuesta -2': 'Error: No se obtuvieron datos.',
                'Respuesta -1001': 'Error: En el metodo de peticion.',
            }, 1
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Resultado': resultado}
        
    def post(self):
        datos, mensaje, resultado = [], '', -1001
        try:
            dictParameters = {
                'Token': {'type': 'str', 'required': True},
                'IdUsuario': {'type': 'int', 'required': True},
                'Modificacion': {'type': 'dt', 'required': True},
            }
            dPV, mensaje, resultado = ValidarParametros(dictParameters, request.get_json())
            if resultado < 1:
                return
            # if not ValidarToken(str(dPV['Token']), int(dPV['IdUsuario'])):
            #     resultado = -1000
            #     return
            datos, resultado = funcion.ObtenerUnidades(Metodo.Rest, dPV['Modificacion'])
        except:
            GetExcept(_Method=Metodo.Rest)
        finally:
            return {'Datos': datos, 'Mensaje': mensaje, 'Resultado': resultado}
#endregion

def Rest():
    try:
        app = Flask(__name__)
        CORS(app, resources={r'/*': {'origins': '*', 'methods': 'GET, POST'}})
        Compress(app)
        api = Api(app)
        api.add_resource(Version_ObtenerVersion, '/{}/Version'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_ObtenerPerfil, '/{}/Catalogo/ObtenerPerfil'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_EditarUsuario, '/{}/Catalogo/EditarUsuario'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_EliminarUsuario, '/{}/Catalogo/EliminarUsuario'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_NuevoUsuario, '/{}/Catalogo/NuevoUsuario'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_ObtenerUsuario, '/{}/Catalogo/ObtenerUsuario'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_EditarUsuario_V2, '/{}/Catalogo/EditarUsuario_V2'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_EliminarUsuario_V2, '/{}/Catalogo/EliminarUsuario_V2'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_NuevoUsuario_V2, '/{}/Catalogo/NuevoUsuario_V2'.format(appConfig.NombreServicio))
        api.add_resource(Catalogo_ObtenerUsuario_V2, '/{}/Catalogo/ObtenerUsuario_V2'.format(appConfig.NombreServicio))

        api.add_resource(Empresa_ObtenerEmpresas, '/{}/Empresa/ObtenerEmpresas'.format(appConfig.NombreServicio))

        api.add_resource(Linker_ObtenerLinkers, '/{}/Linker/ObtenerLinkers'.format(appConfig.NombreServicio))

        api.add_resource(Unidad_ObtenerUnidades, '/{}/Unidad/ObtenerUnidades'.format(appConfig.NombreServicio))
        
        app.run(appConfig.HTTP['Ip'], appConfig.HTTP['Puerto'], False, threaded=True)
    except:
        GetExcept(_Method=Metodo.Rest)


def IniciarRest() -> None:
    try:
        Thread(None, Rest, 'Rest').start()
    except:
        GetExcept(_Method=Metodo.Rest)
