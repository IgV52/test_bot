
from anketa import anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment, anketa_dontknow
from handlers import greet_user, guess_game, planet_name, send_cat_picture, discount_price, talk_to_me, user_coordinats, chek_user_photo
import logging, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)

def main():
    mybot = Updater(settings.API_KEY, use_context = True)

    dp = mybot.dispatcher

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
    
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("dis", discount_price))
    dp.add_handler(CommandHandler("guess", guess_game))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(CommandHandler("planet", planet_name))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.photo, chek_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinats))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info(f"BOT starting... Date: {time.ctime()}")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()