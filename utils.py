
from emoji import emojize
from random import choice, randint
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2



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