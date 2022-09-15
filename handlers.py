from jobs import alarm
from glob import glob
from random import choice
import ephem
import os
from utils import (has_object_on_image, play_random_number, main_keyboard, discount_formula, 
                has_object_on_image, cat_rating_inline_keyboard, get_bot_number)
from db import (db, get_or_create_user, subscribe_user, 
                unsubscribe_user, save_cat_image_vote, user_voted, get_image_rating)


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(f'Здравствуй, пользователь {user["emoji"]}!',
    reply_markup=main_keyboard())

def talk_to_me(update, context):
    text = update.message.text  
    update.message.reply_text(f"{text}",
    reply_markup=main_keyboard())

def guess_game(update, context):
    if context.args:
        try:
            user_num = int(context.args[0])
            bot_num = get_bot_number(user_num)
            message = play_random_number(user_num, bot_num)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message, reply_markup=main_keyboard())

def send_cat_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    cat_photo_list = glob("images/cat*.jp*g")
    cat_pic_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    if user_voted(db, cat_pic_filename, user['user_id']):
        rating = get_image_rating(db, cat_pic_filename)
        caption = f"Рейтинг картинки {rating}"
        reply_markup = None
    else:
        reply_markup = cat_rating_inline_keyboard(cat_pic_filename)
        caption = None
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(cat_pic_filename, 'rb'),
        reply_markup=reply_markup,
        caption=caption
    )

def user_coordinats(update, context):
    coords = update.message.location
    update.message.reply_text(f"Ваши координаты {coords}!",
    reply_makeup=main_keyboard())

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
    update.message.reply_text(message, reply_markup=main_keyboard())

def planet_name(update, context):
    time = update.message.date 
    time = time.strftime("%m/%d/%Y")
    planet = context.args[0]
    try:
        planet = getattr(ephem, planet)(time)
        star = ephem.constellation(planet)
        stars = f"Сегодня находится в созвездии {star[1]}"
        if len(star) == 2:
            update.message.reply_text(stars, reply_markup=main_keyboard())
        else:
            text = "Что то не так..."
            update.message.reply_text(text)  
    except AttributeError as err:
        return update.message.reply_text(f"Ошибка {err}")

def next_full_moon(update, context):
    moon = context.args[0]
    moon_day = ephem.next_full_moon(moon)
    return update.message.reply_text(moon_day)

def chek_user_photo(update, context):
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('donwloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('donwloads', f"{update.message.photo[-1].file_id}.jpg")
    photo_file.download(file_name)
    update.message.reply_text("Файл сохранен")
    if has_object_on_image(file_name, 'cat'):
        update.message.reply_text('Обнаружен котик, сохраняю в библиотеку')
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Котик не обнаружен!')

def word_count(update, context):
    word = context.args
    message = word_chek(word)
    return update.message.reply_text(message)

def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('Вы подписаны')

def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('Вы отменили подписку')

def set_alarm(update, context):
    try:
        alarm_second = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_second, context=update.message.chat.id)
        update.message.reply_text(f'Выполню через {alarm_second}')
    except (ValueError, TypeError):
        update.message.reply_text(f'Проблема')


def cat_picture_rating(update, context):
    update.callback_query.answer()
    callback_type, image_name, vote = update.callback_query.data.split('|')
    vote = int(vote)
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    save_cat_image_vote(db, user, image_name, vote)
    rating = get_image_rating(db, image_name)
    update.callback_query.edit_message_caption(caption=f'Рейтинг картинки {rating}')