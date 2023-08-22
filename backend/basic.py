from datetime import datetime
from os.path import split
import sys


def WriteLog(py: str, method: str, info: str) -> None:
    """
        Escribe archivo log sin dependencias de una configuracion.
    """
    try:
        fecha = datetime.utcnow()
        with open('{}_Critico.log'.format(fecha.strftime('%Y%m%d')), 'a') as file:
            file.write('{} {} {} {}\n'.format(fecha.strftime('%H:%M:%S'), py, method, info))
    except Exception as e:
        with open('error.log', 'w') as file:
            file.write(e)


def GetExcept(_Message: str='') -> None:
    """
        Obtiene el error y manda a escribir un log.
    """
    try:
        errorType, errorMessage, exc_tb = sys.exc_info()
        errorFile = split(exc_tb.tb_frame.f_code.co_filename)[1]
        errorLine = exc_tb.tb_lineno
        errorMethod = '{}()'.format(exc_tb.tb_frame.f_code.co_name)
        WriteLog(errorFile, errorMethod, '{} {} {} {}'.format(errorLine, errorType, errorMessage, _Message))
        del errorType, errorMessage, exc_tb, errorFile, errorLine, errorMethod
    except Exception as e:
        with open('error.log', 'w') as file:
            file.write(e)
