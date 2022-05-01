from datetime import datetime
from db import db, get_subscribe
from telegram.error import BadRequest

def send_updates(context):
    time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    for user in get_subscribe(db):
        try:
            context.bot.send_message(chat_id=user['chat_id'], text=f'Привет {time}')
        except BadRequest:
            print(f"Chat {user['chat_id']} not found")

def alarm(context):
    context.bot.send_message(chat_id=context.job.context, text=f'Все работает')