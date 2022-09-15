from encodings import utf_8
from anketa import anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment, anketa_dontknow
from handlers import (greet_user, guess_game, planet_name, send_cat_picture, discount_price, talk_to_me, unsubscribe, 
                        user_coordinats, chek_user_photo, word_count, next_full_moon, subscribe, set_alarm, cat_picture_rating)
import logging
import pytz
from datetime import time, datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram.ext import messagequeue as mq
from telegram.bot import Bot
from telegram.utils.request import Request
from jobs import send_updates
from game_city import gm_start, play
import gamecity


import settings

logging.basicConfig(filename="bot.log", level=logging.INFO, encoding="utf_8")

class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, msg_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = msg_queue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super().send_message(*args, **kwargs)

def main():
    with open("city.txt", "r", encoding='utf-8') as f:
        db_city = [city for city in f.readlines()]

    formated_db_city = gamecity.GameCity.form_list_city(db_city)
    gamecity.GameCity.city_list = formated_db_city
    
    request = Request(con_pool_size=8)
    bot = MQBot(settings.API_KEY, request=request)
    mybot = Updater(bot=bot, use_context = True)

    dp = mybot.dispatcher
    jq = mybot.job_queue
    target_days = range(3)
    target_time = time(12,0, tzinfo=pytz.timezone('Europe/Moscow'))
    jq.run_daily(send_updates, target_time, target_days)

    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex("^(Заполнить анкету)$"), anketa_start)
        ], 
        states={"name" : [MessageHandler(Filters.text, anketa_name)],
                "rating" : [MessageHandler(Filters.regex("^(1|2|3|4|5)$"), anketa_rating)],
                "comment" : [CommandHandler("skip", anketa_skip), 
                            MessageHandler(Filters.text, anketa_comment)]
        }, 
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, anketa_dontknow)
        ]
    )

    gcity = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex("^(Играть)$"), gm_start)
        ], 
        states={"play" : [MessageHandler(Filters.text, play)]
        }, 
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, anketa_dontknow)
        ]
    )
    
    dp.add_handler(anketa)
    dp.add_handler(gcity)
    dp.add_handler(CallbackQueryHandler(cat_picture_rating, pattern="^(rating|)"))
    dp.add_handler(CommandHandler('alarm', set_alarm))
    dp.add_handler(CommandHandler('sub', subscribe))
    dp.add_handler(CommandHandler('unsub', unsubscribe))
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("dis", discount_price))
    dp.add_handler(CommandHandler("guess", guess_game))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(CommandHandler("planet", planet_name))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.photo, chek_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinats))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info(f"BOT starting... Date: {datetime.now()}")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()