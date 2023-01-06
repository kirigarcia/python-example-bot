from config import * #importamos el token
import telebot #para manejar la api de telegram
import time
import threading

#instanciamos el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

#responde al comando /start, /help y /ayuda
@bot.message_handler(commands= ['start', 'ayuda', 'help'])
def cmd_start(message):
    '''Da  la bienvenida al usuario del bot'''
    bot.reply_to(message,'hey,  bienvenido')
    print(message.chat.id)
'''
responde a los sms de texto q no sean comandos
text, audio, documento,photo,sticker, video,video_note,voice, location,
contact, new_chat_members, left_chat_member, new_chat_title, new_chat_photo,
delete_chat_photo,group_chat_created, supergroup_chat_created, channel_chat_created,
migrate_to_chat_id, migrate_from_chat_id, pinned_message
'''
@bot.message_handler(content_types=['text', "photo"])
def bot_mensajes_texto(message):
    '''Gestiona los mensajes de texto recibidos'''
    #formatos HTML
    texto_HTML='<b><u>Formatos HTML</u>:</b>'+ '\n' #negrita y subrayado en HTML
    texto_HTML+='<b>NEGRITA</b>'+ '\n' #negrita  en HTML
    texto_HTML+='<i>CURSIVA</i>'+ '\n' #cursiva  en HTML
    texto_HTML+='<u>SUBRAYADO</u>'+ '\n' #subrayado en HTML
    texto_HTML+='<s>TACHADO</s>'+ '\n' #tachado  en HTML
    texto_HTML+='<code>MONOESPACIADO</code>'+ '\n' #monoespaciado  en HTML
    texto_HTML+='<span class ="tg-spoiler">SPOILER</span>'+ '\n' #spoiler en HTML
    texto_HTML+='<a href = "https://www.frikidelto.com/">ENLACE</a>'+ '\n' #enlace  en HTML

    '''
    #formatos MarkdownV2
    texto_markdown='*__Formatos Markdown__:*' +'\n'
    texto_markdown+='*NEGRITA*' +'\n'
    texto_markdown+='_CURSIVA_' +'\n'
    texto_markdown+='__SUBRAYADO__' +'\n'
    texto_markdown+='~TACHADO~' +'\n'
    texto_markdown+='´´MONOESPACIADO´´' +'\n'
    texto_markdown+='||SPOILER||' +'\n'
    texto_markdown+='[ENLACE](https://www.frikidelto.com/)' +'\n'
    '''
    if message.text and message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Comando no disponible')
    else:
        '''
        x = bot.send_message(message.chat.id, '<b>HOLA</b>', parse_mode ='html', disable_web_page_preview = True)
        bot.send_message(message.chat.id, texto_markdown, parse_mode ='MarkdownV2', disable_web_page_preview = True)
        time.sleep(3)
        bot.edit_message_text('<u>ADIÓS</u>',message.chat.id, x.message_id, parse_mode='html' )
        bot.delete_message(message.chat.id, x.message_id)
        Si el mensaje que queremos eliminar es el pone el usuario
        bot.delete_message(message.chat.id, message.message_id)
        '''
        #enviar una foto
        '''
        foto = open("./imagenes/FB_IMG_15900692858196070.jpg", 'rb')
        bot.send_photo(message.chat.id, foto, 'PELÓN!!!')
        
        #enviar un archivo
        archivo = open("./docs/Tribunales de Tesis 2022.xlsx", 'rb')
        bot.send_document(message.chat.id, archivo, caption= 'Qué buena guía!!!')
        '''

        #enviar un video 
        'typing', 'upload_photo', 'record_video', 'upload_video', 'record_audio', 'upload_audio'
        'upload_document', 'find_location', 'record_video_note','upload_video_note'
        bot.send_chat_action(message.chat.id, 'upload_video' )
        archivo = open("./video/este video de Minecraft dura 3 segundos.mp4", 'rb')
        bot.send_video(message.chat.id, archivo, caption= 'vaya vaya!!!')


def recibir_mensajes():
    '''Bucle infinito que comprueba si hay nuevos mensajes'''
    bot.infinity_polling()

#MAIN   
if __name__=='__main__':
    #configuramos los comandos disponibles del bot
    bot.set_my_commands([
        telebot.types.BotCommand('/start', 'da la bienvenida'),
        telebot.types.BotCommand('help', 'ayuda')
    ])
    print('Iniciando el bot')
    hilo_bot = threading.Thread(name= 'hilo_bot', target= recibir_mensajes)
    hilo_bot.start()
    print('Bot iniciado')
    bot.send_message(MI_CHAT_ID, 'Python me gusta cantidad!!!')
    
