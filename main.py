import time
from threading import Thread

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import bottoken
import work_db as db


session = vk_api.VkApi(token=bottoken)
flag_add, flag_delete = False, False


#timer and del
def sleep_note(id_note, x, user_id):
    time.sleep(x)
    send_msg(user_id, db.out_text_note(id_note))
    db.del_note(id_note)


#thread
def thread_notes(id_note, time_sleep, user_id):
    th = Thread(target=sleep_note, args=(id_note, time_sleep, user_id, ))
    th.start() 


#send message to chat (with keyboard)
def send_msg(user_id, message, keyboard=None):
    post = {
        "peer_id": user_id,
        "message": message,
        "random_id": 0
    }
        
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
        
    session.method('messages.send', post)


#commands of bot
def command(user_id, text):
    global flag_add, flag_delete
    if text == '/start':
        start(user_id)      
    elif text == 'добавить':
        flag_add = True
        add_note(user_id)
    elif text == 'удалить':
        flag_delete = True
        delete_note(user_id)
    elif text == 'список':
        output_notes(user_id)
    elif text == 'отмена':
        start(user_id)
    elif (flag_add and text):
        add_commands(user_id, text)
    else:
        if text == 'выберите действие': pass
        else:
            send_msg(user_id, "Не понимаю о чем идет речь\n Введите /start для начала работы с ботом")
            
    
#start bot (first keyboard)
def start(user_id):
    global flag_add, flag_delete
    flag_add, flag_delete = False, False
    keyboard = VkKeyboard()
    keyboard.add_button('Добавить', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Удалить', VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Список', VkKeyboardColor.SECONDARY)
    send_msg(user_id, 'Выберите действие', keyboard)


#add note to DB
def add_note(user_id):
    keyboard_add = VkKeyboard(one_time=True)
    keyboard_add.add_button('1', VkKeyboardColor.PRIMARY)
    keyboard_add.add_button('2', VkKeyboardColor.PRIMARY)
    keyboard_add.add_button('3', VkKeyboardColor.PRIMARY)
    keyboard_add.add_line()
    keyboard_add.add_button('Отмена', VkKeyboardColor.NEGATIVE)
    send_msg(user_id, 'Выберите тип напоминания', keyboard_add) 


#commands for types
def add_commands(user_id, text):
    if text == '1':
        send_msg(user_id, 'Введите дату и напоминание')
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                user_id = event.user_id
                id_note, timer = db.input_note(text)
                thread_notes(id_note, timer, user_id)
                break
    if text == '2':
        send_msg(user_id, 'Введите дату и напоминание')
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                user_id = event.user_id
                id_note, timer = db.input_note(text)
                thread_notes(id_note, timer, user_id)
                break
    if text == '3':
        send_msg(user_id, 'Введите дату и напоминание')
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                user_id = event.user_id
                id_note, timer = db.input_note(text)
                thread_notes(id_note, timer, user_id)
                break
    start(user_id)      


#delete note from DB
def delete_note(user_id):
    send_msg(user_id, 'DELETE')
    output_notes(user_id)
    send_msg(user_id, "Введите id для удаления:") 
    for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text
                user_id = event.user_id
                db.del_note(text)
                break
    start(user_id)


#show notes from DB
def output_notes(user_id):
    send_msg(user_id, db.out_notes())


def main():        
    print('Bot active!')

    #chat looping
    for event in VkLongPoll(session).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.lower()
            user_id = event.user_id

            command(user_id, text)
            
          
if __name__ == '__main__':
    run_notes = db.update_time()
    for key, value in run_notes.items():
        thread_notes(key, value, 115250642)

    main()