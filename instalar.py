from backend.configuracion import appConfig, Inicia, ObtenerConfiguracion, MensajePrecaucion
from backend.archivo import CrearArchivoSistema
from backend.entidades import Evento, Servicio
from sys import exit


if __name__ == '__main__':
    dicPropiedades = ObtenerConfiguracion('app.json')
    if dicPropiedades is None:
        MensajePrecaucion(Evento.Error, 'ObtenerConfiguracion()', 'El Servicio no iniciara por que no se ha configurado correctamente 1.')
        exit(0)
    if not Inicia(Servicio.Servicio, dicPropiedades, False):
        MensajePrecaucion(Evento.Error, 'Iniciar()', 'El Servicio no iniciara por que no se ha configurado correctamente 2.')
        exit(0)
    print(CrearArchivoSistema(appConfig.Ambiente.name, appConfig.IdServicio, appConfig.IdInstalacion, appConfig.NombreServicio, appConfig.Descripcion))

