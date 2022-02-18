from glob import glob
from random import choice
import ephem
import os
from utils import get_smile, has_object_on_image, play_random_number, main_keyboard, discount_formula, has_object_on_image

def greet_user(update, context):
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!",
    reply_markup=main_keyboard())

def talk_to_me(update, context):
    text = update.message.text  
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(f"{text} {context.user_data['emoji']}",
    reply_markup=main_keyboard())

def guess_game(update, context):
    if context.args:
        try:
            user_num = int(context.args[0])
            message = play_random_number(user_num)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message, reply_markup=main_keyboard())

def send_cat_picture(update, context):
    cat_photo_list = glob("images/cat*.jp*g")
    cat_pic_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, "rb"), reply_markup=main_keyboard())

def user_coordinats(update, context):
    context.user_data["emoji"] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(f"Ваши координаты {coords} {context.user_data['emoji']}!",
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
    planet = getattr(ephem, planet)(time)
    star = ephem.constellation(planet)
    stars = f"Сегодня находится в созвездии {star[1]}"
    if len(star) == 2:
      update.message.reply_text(stars, reply_markup=main_keyboard())
    else:
      text = "Что то не так..."
      update.message.reply_text(text)  

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