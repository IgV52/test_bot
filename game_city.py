from telegram import ReplyKeyboardRemove
from gamecity import Player, Bot, GameCity

def gm_start(update, context):
    player_1 = Player(name=update.effective_user.username)
    player_2 = Bot('Bot')
    players = [player_1, player_2]
    game = GameCity(players)
    context.user_data['gmcity'] = game
    context.user_data['Player'] = player_1
    context.user_data['Bot'] = player_2
    info = game.start()
    if game.step == player_2:
        city = player_2.step
        game.play()
        x = game.start()
        info = f"{info} {city} \n {x}"
    update.message.reply_text(f"{info}",reply_markup=ReplyKeyboardRemove())
    return "play"

def play(update, context):
    context.user_data['Player'].city = update.message.text
    context.user_data['gmcity'].play()
    info = context.user_data['gmcity'].start()
    city = context.user_data['Bot'].step
    context.user_data['gmcity'].play()
    x = context.user_data['gmcity'].start()
    info = f"{info} {city} \n {x}"
    update.message.reply_text(f"{info}",reply_markup=ReplyKeyboardRemove())
    return "play"

