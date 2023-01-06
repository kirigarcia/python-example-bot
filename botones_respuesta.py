from config import *
import telebot #para manejar la api de telegram
from telebot.types import ReplyKeyboardMarkup #para crear botones
from telebot.types import ForceReply # para citar mensajes
from telebot.types import ReplyKeyboardRemove #para eliminar botones
from random import randint # para generar numeros aleatorios enteros
#botones inline
from telebot.types import InlineKeyboardMarkup  # para crear botonera inline
from telebot.types import InlineKeyBoardButton  # para definir botones inline


#instanciamos el bot de telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)
#variable global en la que guardaremos los datos del usuario 
usuarios = {}

#responde al comando /start, /help y /ayuda
@bot.message_handler(commands= ['start', 'ayuda', 'help'])
def cmd_start(message):
    '''Muestra los comandos disponibles'''
    botones = ReplyKeyboardRemove()   #para eliminar botones
    bot.send_message(message.chat.id, 'Usa el comando /jugar para empezar', reply_markup= botones)

#responde al comando /jugar
@bot.message_handler(commands= ['jugar'])
def cmd_jugar(message):
    """Inicia el juego """
    numero = randint(1,10)
    cid = message.chat.id
    usuarios[cid] = numero 
    botones = ReplyKeyboardMarkup(input_field_placeholder = "Pulsa un botón")
    row_width = 5
    #botones.add('1', '2', '3', '4', '5', '6','7', '8', '9', '10')
    botones.row('1')
    botones.row('2','3')
    botones.row('4','5','6')
    botones.row('7','8','9','10')
    msg = bot.send_message(message.chat.id, 'Adivina el número entre1 y 10', reply_markup = botones)
    #resgistramos la respuesta en la funcion indicada
    bot.register_next_step_handler(msg, comprobar_numero)


def comprobar_numero(message):
    '''Compruebe si el número es correcto'''
    cid= message.chat.id
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, 'ERROR: Introduce un número')
        bot.register_next_step_handler(msg, comprobar_numero)
    else:
        n = int(message.text)
        if n<1 or n>10:
            msg = bot.send_message(message.chat.id, 'ERROR: Número fuera de rango')
            bot.register_next_step_handler(msg, comprobar_numero)
        else:
            if n == usuarios[cid]:
                markup = ReplyKeyboardRemove()
                bot.reply_to(message, '!!!Ha acertado, felicidades!!!', reply_markup = markup)
                return
            elif n > usuarios[cid]:
                msg = bot.reply_to(message,'Pista: Es menor')
                bot.register_next_step_handler(msg, comprobar_numero)
            else:
                msg = bot.reply_to(message,'Pista: Es mayor')
                bot.register_next_step_handler(msg, comprobar_numero)
"""
#rwsponde al comando /alta
@bot.message_handler(commands = ['alta'])
def cmd_alta(message):
    '''Pregunta el nombre del usuario y responde un mensaje en concreto'''
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, '¡Cómo te llamas!', reply_markup= markup)
    bot.register_next_step_handler(msg, preguntar_edad)

def preguntar_edad(message):
    '''Preguntar la edad del usuario'''
    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]['nombre'] = message.text
    markup = ForceReply()
    msg = bot.send_message(message.chat.id, '¡Cuántos años tienes!', reply_markup= markup)
    bot.register_next_step_handler(msg, preguntar_sexo)

def preguntar_sexo(message):
    '''Preguntar el sexo del usuario'''
    #si la edad introducida no es un numero
    if not message.text.isdigit():
        #informamos el error y volver a preguntar
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, 'ERROR: Debes indicar un número. \n ¿Cuàntos años tienes?', reply_markup= markup)
        #volvemos a ejecutar esta función
        bot.register_next_step_handler(msg, preguntar_sexo)
    else: #si se introdujo la edad correctamente
        usuarios[message.chat.id]['edad'] =int(message.text)
        #definimos 2 botones
        markup = ReplyKeyboardMarkup(
            one_time_keyboard= True,
            input_field_placeholder= 'Pulsa un botón',
            resize_keyboard = True
            )
        markup.add('Hombre', 'Mujer')
        #Preguntamos por el sexo
        msg = bot.send_message(message.chat.id, '¿Cuàl es tu sexo?', reply_markup = markup ) 
        #registramos la respuesta en la función indicada
        bot.register_next_step_handler(msg, guardar_datos_usuario)

def guardar_datos_usuario(message):
    #Guardamos los datos introducidos por el usuario
    #si el sexo introducido no es válido
    if message.text != 'Hombre' and message.text != 'Mujer':
        #informamos el error y volvemos a preguntar
        msg = bot.send_message(message.chat.id, 'ERROR: Sexo no válido.\n Pulsa un botón')
        #volvemos a ejecutar esta funcion 
        bot.register_next_step_handler(msg, guardar_datos_usuario)
    else: #si el sexo introducido no es válido 
        usuarios[message.chat.id]['sexo'] = message.text 
        texto = 'Datos introducidos:\n'
        texto+= f'<code>NOMBRE:</code> {usuarios[message.chat.id]["nombre"]}\n'
        texto+= f'<code>EDAD:</code> {usuarios[message.chat.id]["edad"]}\n'
        texto+= f'<code>SEXO:</code> {usuarios[message.chat.id]["sexo"]}\n'
        markup = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, texto, parse_mode = "html")
        print(usuarios)
        del usuarios[message.chat.id]
"""


#MAIN ####################
if __name__=='__main__':
    print('Iniciando BOT...')
    #bucle infinito en el que se comprueba si hay nuevos mensajes
    bot.infinity_polling()
