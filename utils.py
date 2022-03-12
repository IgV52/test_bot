
from email import message
from emoji import emojize
from random import choice, randint
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
import csv


def discount_formula(user_price, user_discount):
    if user_discount >= 100:
        message = f"Итоговая цена {user_price}"
    else:
        final_price = user_price - (user_price * user_discount / 100)
        message = f"Итоговая цена {final_price}"
    return message

def play_random_number(user_num):
    bot_num = randint(user_num - 10, user_num + 10)
    if user_num > bot_num:
        message = f"Ваше число {user_num}, мое {bot_num}, вы выиграли!"
    elif user_num == bot_num:
        message = f"Ваше число {user_num}, мое {bot_num}, ничья!"
    else:
        message = f"Ваше число {user_num}, мое {bot_num}, вы проиграли!"
    return message

def main_keyboard():
    return ReplyKeyboardMarkup([["Прислать котика", KeyboardButton('Мои координаты', request_location=True), "Заполнить анкету"]])


def has_object_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)
    
    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(image=image)
            )
        ])
    response = app.PostModelOutputs(request, metadata=metadata)
    return check_response_for_object(response, object_name)

def check_response_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.85:
                return True
    else:
        print(f'Ошибка распознавания картинки {response.outputs[0].status.details}')
    return False

def word_chek(text):
    counter = 0
    for word in text:
        if word.isalpha():    
            counter += 1
    message = f'Количество слов равно {counter}'
    return message

def check_symbol(city):
    wrong_char = ("Ъ", "ь", "ы", "й")
    for char in city[::-1]:
        if char in wrong_char:
            continue
        else:
            break
    else:
        raise RuntimeError
    return char

def search_city(user, city):
    city = format_city(city)
    check = check_base_game(user, city)
    if check:
        cities = open_base_city()
        for line_user in cities:
            line_user = format_city(line_user)
            if line_user in city:
                variant_bot = city
                variant_bot = check_symbol(variant_bot)
                for line_bot in cities:
                    line_bot = format_city(line_bot)
                    if line_bot[0] == variant_bot:
                        message = line_bot.capitalize()
                        create_base_use_city(user, city, message)
                        break  
    else:
        message = 'Этот город был'
    return message

def check_base_game(user, city):
    with open('city_game.csv', 'r', encoding='utf-8') as f:
        cities = {city for city in f.readlines() if city.strip()}
        good = True
        for line in cities:
            lines = line.replace('\n', '').split(',')
            if lines[0] == str(user) and lines[1] == city:
                good = False
                break
            if lines[0] == str(user) and lines[2] == city:
                good = False
                break
        return good

def format_city(city):
    return city.strip().lower().replace('ё','е').replace('\n',"")

def open_base_city():
    with open("city.txt", "r", encoding='utf-8') as f:
        cities = {format_city(city) for city in f.readlines() if city.strip()}
        return cities

def create_base_use_city(user, city, bot_city):
    with open("city_game.csv", "r+", encoding='utf-8') as f:
        fields = ["user_id", "user_city", "bot_city"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow({'user_id' : user, 'user_city' : city, 'bot_city' : bot_city})
        

def check_city(city_check):
    city_check = city_check.lower()
    cities = open_base_city()
    for city in cities:
        if city == city_check:
            proverka = 1
            break
        else:
            proverka = 0
    return proverka

