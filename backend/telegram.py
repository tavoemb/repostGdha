from backend.entidades import Empresa, MimeType, Telegram
from backend.configuracion import appConfig
from backend.basic import GetExcept
from telebot import TeleBot
from requests import post


dictTB = {
    Empresa.Elevenminds: {
        Telegram.Advertencias: {
            'Canal': -1001659235044,
            'Token': '5435539832:AAExN4EbJdD_TGqFIIMM4uQB65i2wzNRwfs'
        },
        Telegram.Alertas: {
            'Canal': -1001596381690,
            'Token': '5424583621:AAGljgwr0ap9E_3BA-Y072e2e1N29e2nLhU'
        },
        Telegram.Errores: {
            'Canal': -1001712601119,
            'Token': '5529340212:AAGspHirM0JykX6UpbgYnEiu73w5ii4Sbhc'
        },
        Telegram.Monitoreo: {
            'Canal': -1001884507305,
            'Token': '6019093323:AAGafFjsqAP_SU-KFr_9xc2MqHU8aEd78H0'
        },
    },
    Empresa.GlobalTrack: {
        Telegram.Advertencias: {
            'Canal': -1001795168245,
            'Token': '5544294303:AAGc4Qqe6NzScjbE4thu5h9Ho_CdokQhajs'
        },
        Telegram.Alertas: {
            'Canal': -1001749652934,
            'Token': '5415207893:AAFHj7SLWm4kGdknbfURmW_jRRk1WToaAJ0'
        },
        Telegram.Errores: {
            'Canal': -1001633050823,
            'Token': '5193588652:AAHlDIg9VTiTVIreVxHxNeoPyPpdKULS6iE'
        },
        Telegram.Monitoreo: {
            'Canal': -1001811195428,
            'Token': '5813211680:AAFwtRpqKoycUflVmPNo57vTVS1v6YxuefQ'
        },
    },
    Empresa.Innovalinks: {
        Telegram.Advertencias: {
            'Canal': -1001368959710,
            'Token': '5518430529:AAGnsQokP9hZ5JlPmiei5EJXwoAfSXZXv3o'
        },
        Telegram.Alertas: {
            'Canal': -1001747154887,
            'Token': '5402539298:AAFdy61AC00w6cflH5vwdeA28Tx69aETdUI'
        },
        Telegram.Errores: {
            'Canal': -1001580960567,
            'Token': '5365276604:AAH8ri14GfwxyErK1-pnRAMzcRccktsiLj4'
        },
        Telegram.Monitoreo: {
            'Canal': -1001758782944,
            'Token': '5731208324:AAEOPfvBuC4LTet5eDk1QKXvba2t7rjF-n4'
        },
    },
    Empresa.SisTechnologies: {
        Telegram.Advertencias: {
            'Canal': -1001522626728,
            'Token': '5469126652:AAETNzXh2iX0rIgCvj7ZRYHut6kYpGaeQ1c'
        },
        Telegram.Alertas: {
            'Canal': -1001687494948,
            'Token': '5519477185:AAETh1MIw75lJqGO4yata9PzKG4PdD5Xkws'
        },
        Telegram.Errores: {
            'Canal': -1001548743106,
            'Token': '5366032383:AAECVZ5Xs84aM0SEBip53pbLnDe46WbXziI'
        },
        Telegram.Monitoreo: {
            'Canal': -1001786765223,
            'Token': '5848831995:AAGVpRJCxTqyaG6owojhfUv-uqJSTYN-xio'
        },
    },
    Empresa.TheRightConnectionsDeMexico: {
        Telegram.Advertencias: {
            'Canal': -1001857754830,
            'Token': '5754080542:AAEzdr47ipn7dcKMQ6sieGNrwpt5EJR-Zw0'
        },
        Telegram.Alertas: {
            'Canal': -1001687058057,
            'Token': '5684098461:AAE2X2hocSHll0RJQ5wj2aiFMC9xYx7PS4c'
        },
        Telegram.Errores: {
            'Canal': -1001836482865,
            'Token': '5723332723:AAGm40D0Y7oXvUGw4XPcOdzLINDs0Ava92c'
        },
        Telegram.Monitoreo: {
            'Canal': -1001871155825,
            'Token': '5987814274:AAHweqyejg_eGns2MutUdbt5ozxaKfJCh70'
        },
    }
}


def SendMessage(_Text: str, _Tipo=Telegram.Errores, _Token=None, _IdCanal=None, _Mode=MimeType.MarkdownV2, _Markup=None, _Method='', _Subjspy=True) -> int:
    """
        Envia un mensaje por telegram.
    """
    resultado = -1
    try:
        tb = TeleBot(_Token if _Tipo == Telegram.Especifico else dictTB[appConfig.Empresa][_Tipo]['Token'], threaded=False)
        resultado = tb.send_message(_IdCanal if _Tipo == Telegram.Especifico else dictTB[appConfig.Empresa][_Tipo]['Canal'], _Text, parse_mode=_Mode.name, reply_markup=_Markup).message_id
        del tb
    except:
        resultado = -2
        _Text = _Text.replace('🟢', '').replace('🔴', '')
        GetExcept('{} _ {}'.format(_Method, _Text))
        if _Subjspy:
            try:
                post('https://rest1.elevenminds.emback.xyz/SUBJs/Enviar/Telegram', json={'Empresa': appConfig.Empresa.value, 'Tipo': _Tipo.value, 'Marcado': _Mode.name, 'Texto': _Text})
            except:
                pass
    finally:
        return resultado


def SendMessageImage(_Text: str, _Img: str, _Tipo=Telegram.Errores, _Token=None, _IdCanal=None, _Mode=MimeType.MarkdownV2, _Markup=None) -> int:
    """
        Envia un mensaje por telegram con imagen.
    """
    resultado = -1
    try:
        photo = open(_Img, 'rb')
        tb = TeleBot(_Token if _Tipo == Telegram.Especifico else dictTB[appConfig.Empresa][_Tipo]['Token'], threaded=False)
        resultado = tb.send_photo(_IdCanal if _Tipo == Telegram.Especifico else dictTB[appConfig.Empresa][_Tipo]['Canal'], photo, _Text, parse_mode=_Mode.name, reply_markup=_Markup).message_id
        del tb
    except:
        _Text = _Text.replace('🟢', '').replace('🔴', '')
        GetExcept(_Text)
        resultado = -2
    finally:
        return resultado


def Negritas(_str: str) -> str:
    """
        Envuelve el objeto string para ponerlo
        en negrita para mensaje de telegram.
    """
    return '**{}**'.format(_str)


def Mono(_str: str) -> str:
    """
        Envuelve el objeto string para ponerlo
        en tipo mono para mensaje de telegram.
    """
    return '`{}`'.format(_str)


def SaltoLineal(_str: str) -> str:
    """
        Envuelve el objeto string para ponerlo con
        un salto de linea para mensaje de telegram.
    """
    return '{}\n'.format(_str)


def EscapeCharacters(_Text: str) -> str:
    """
        Escapa los caracteres que esten excluidos en la lista de marcado de telegram.

        Args:
            _Text (str): Texto a procesar.

        Returns:
            resultado (str): Texto con caracteres escapados.
    """
    resultado = ''
    try:
        for letter in str(_Text):
            if letter in  ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!', '\\'):
                resultado += '\{}'.format(letter)
            else:
                resultado += letter
    except:
        pass
    return resultado
