from config import *
import telebot
#botones inline
from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton  # para crear botonera inline, para definir botones respectivamente
import requests
# from bs4 import BeautifulSoup




#instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

#responde al comando /botones
@bot.message_handler(commands=['botones'])
def cmd_botones(message):
    '''Muestra un mensaje con botones inline(a continuación del mensaje)'''
    markup = InlineKeyboardMarkup (row_width=2)  #numero de botones en cada fila(3 por defecto)
    b1 = InlineKeyboardButton ('TOP Descuentazos', url= 'https://t.me/top_descuentazos')
    b2 = InlineKeyboardButton ('TOP AMZ', url= 'https://t.me/top_amz')
    b3 = InlineKeyboardButton ('TOP Todo China', url= 'https://t.me/top_todo_china')
    b4 = InlineKeyboardButton ('TOP Cupones', url= 'https://t.me/top_cupones')
    b5 = InlineKeyboardButton ('TOP Ofertas', url= 'https://t.me/frikidelto_chollos')
    b_cerrar = InlineKeyboardButton('CERRAR',callback_data= 'cerrar')
    markup.add(b1, b2, b3, b4, b5, b_cerrar)
    bot.send_message(message.chat.id, 'Mis canales de ofertas👌', reply_markup = markup)

@bot.callback_query_handler(func = lambda x: True )
def respuesta_botones_inline(call):
    '''Gestiona las acciones de los botones callback_data'''
    cid = call.from_user.id
    mid = call.message.id
    if call.data == 'cerrar':
        bot.delete_message(cid, mid)

#responde al comando /buscar
@bot.message_handler(commands=['buscar'])
def cmd_buscar(message):
    '''Realiza una búsqueda en Google y devuelve una lista de resultados
    con la siguiente estructura[[titulo, url],[título, url]....]'''
    texto_buscar = ' '.join(message.text.split()[1:])
    #si no se han pasado parámetros 
    if not texto_buscar:
        texto = 'Debes introducir una búsqueda. \n'
        texto+= 'Ejemplo: \n'
        texto+= f'<code>{message.text} lionelmessi</code>'
        bot.send_message(message.chat.id, texto, parse_mode ='html')
        return 1
    #si se ha indicado un texto de búsqueda
    else:
        print(f'Buscando en Google: "{texto_buscar}"')
        url = f'https://www.google.com/search?q={texto_buscar.replace("", "+")}&num=100'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Unique/93.7.1196.97'
        headers = {'user-agent': user_agent}
        res = request.get(url, headers =headers, timeout = 10)
        if res.status_code!= 200:
            print(f'ERROR al buscar: {res.status_code} {res.reason}')
            bot.send_message(message.chat.id, texto, 'Se ha producido un error. Inténtelo más tarde')
            return 1
        else:
            pass
            # soup = BeautifulSoup(res.text, 'html.parser')
            # elementos = soup.find_all('div', class_='g')
            # lista = []
            # for elemento in elementos:
            #     try:
            #         titulo = elemento.find('h3').text
            #         url = elemento.find('a').attrs.get('href')
            #         if not url.startswith('http'):
            #             url = 'https://google.es'+ url
            #         if [titulo, url] in lista:
            #             continue
            #         lista.append([titulo, url])
            #     except:
            #         continue
            # print(lista)


#MAIN ####################
if __name__=='__main__':
    print('Iniciando BOT...')
    #bucle infinito en el que se comprueba si hay nuevos mensajes
    bot.infinity_polling()