from utils import get_bot_number, play_random_number

def test_get_bot_number():
    user_number = 10
    assert (user_number - 10) <= get_bot_number(user_number) <= (user_number + 10)

def test_play_random_numbers_win():
    user_num = 10
    bot_num = 5
    assert play_random_number(user_num, bot_num) == f"Ваше число {user_num}, мое {bot_num}, вы выиграли!"

def test_play_random_numbers_lose():
    user_num = 5
    bot_num = 10
    assert play_random_number(user_num, bot_num) == f"Ваше число {user_num}, мое {bot_num}, вы проиграли!"

def test_play_random_numbers_friend():
    user_num = 5
    bot_num = 5
    assert play_random_number(user_num, bot_num) == f"Ваше число {user_num}, мое {bot_num}, ничья!"