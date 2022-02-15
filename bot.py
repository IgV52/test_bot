from glob import glob
from emoji import emojize
import logging, time
import emoji
import ephem
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)

def greet_user(update, context):
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!")
def talk_to_me(update, context):
    text = update.message.text  
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(f"{text} {context.user_data['emoji']}")

def discount_formula(user_price, user_discount):
    if user_discount >= 100:
        message = f"Итоговая цена {user_price}"
    else:
        final_price = user_price - (user_price * user_discount / 100)
        message = f"Итоговая цена {final_price}"
    return message

def get_smile(user_data):
    if "emoji" not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)  
    return user_data["emoji"]

def discount_price(update, context):
    if context.args:
        try:
            user_price = abs(int(context.args[0]))
            user_discount = abs(int(context.args[1]))
            message = discount_formula(user_price, user_discount)
        except (TypeError, ValueError, ZeroDivisionError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)


def play_random_number(user_num):
    bot_num = randint(user_num - 10, user_num + 10)
    if user_num > bot_num:
        message = f"Ваше число {user_num}, мое {bot_num}, вы выиграли!"
    elif user_num == bot_num:
        message = f"Ваше число {user_num}, мое {bot_num}, ничья!"
    else:
        message = f"Ваше число {user_num}, мое {bot_num}, вы проиграли!"
    return message

def guess_game(update, context):
    if context.args:
        try:
            user_num = int(context.args[0])
            message = play_random_number(user_num)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photo_list = glob("images/cat*.jp*g")
    cat_pic_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, "rb"))

def planet_name(update, context):
    time = update.message.date 
    time = time.strftime("%m/%d/%Y")
    planet = context.args[0]
    planet = getattr(ephem, planet)(time)
    star = ephem.constellation(planet)
    stars = f"Сегодня находится в созвездии {star[1]}"
    if len(star) == 2:
      update.message.reply_text(stars)
    else:
      text = "Что то не так..."
      update.message.reply_text(text)  


def main():
    mybot = Updater(settings.API_KEY, use_context = True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("dis", discount_price))
    dp.add_handler(CommandHandler("guess", guess_game))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(CommandHandler("planet", planet_name))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info(f"BOT starting... Date: {time.ctime()}")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()