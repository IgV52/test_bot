
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

def search_city(user, city):
    with open('city_game.csv', 'r+', encoding='utf_8') as city_game, open("city.txt", "r", encoding="utf_8") as city_base:
        fields = ["user_id", "user_city", "bot_city"]
        city = (city.lower()).replace('\n', "")
        for line in city_base:
            line = ((line.lower()).strip()).replace('\n', "")
            if line in city:
                variant_bot = city[-3]
                city_base.seek(0, 0)
                for line_bot in city_base:
                    line_bot = line_bot.replace('\n', "")
                    if line_bot[0].lower() == variant_bot and line_bot.lower() != city:
                        for line_bot_check in city_game:
                            if line_bot_check not in line_bot:
                                bot_city = line_bot.replace('\n', "") 
                                writer = csv.DictWriter(city_game, fieldnames=fields)
                                writer.writeheader()
                                writer.writerow({'user_id' : user, 'user_city' : city, 'bot_city' : bot_city})
                                message = bot_city
            else:
                message = 'Я называл этот город'
        return message

def check_city(city_check):
    city_check = (city_check.lower()).strip()
    city_check = city_check[2:-2]
    with open('city.txt', 'r', encoding='utf_8') as c_check:
        for line in c_check:
            line = ((line.lower()).strip()).replace('\n', "")
            if line == city_check:
                proverka = 1
                break
            else:
                proverka = 0
        return proverka
