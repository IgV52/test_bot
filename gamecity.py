from random import choice

class GameCity:
    city_list = list()
    __wrong_char = ("Ъ", "ь", "ы", "й")
    
    def __init__(self, players: list) -> object:
        self.__check_arg_init(players)
        self.__players = self.__connect(players)
        self.__char = None
        self.__city_used = dict()
        self.__last_city = None
        self.__status_game = None
        self.__step = None

    def __check_arg_init(self, players: list) -> bool:
        if type(players) != list:
            raise TypeError("Это не список, должен быть список игроков")
        if len(players) != 2:
            raise TypeError("Игроков должно быть 2")

    def __connect(self, players: list) -> list:
        for player in players:
            player.connect = self
        return players
    
    def __disconnect(self, players: list) -> None:
        for player in players:
            player.city = None
            player.connect = None
        self.__step = None
        self.__status_game = None
        self.__char = None
        self.__last_city = None
        self.__players.clear()
        self.__city_used.clear()

    def start(self) -> str:
        if not self.__last_city:
            self.__step = choice(self.__players)
            self.__status_game = f"Первый ходит {self.__step.name}"
        else:
            self.__char = self.validate_char(self.__last_city)
            self.__status_game = f"Ходит {self.__step.name} должен назвать город на {self.__char.capitalize()}"
        return self.__status_game

    def play(self) -> None:
        self.__check_connect()
        self.__step.city = self.form_word_city(self.__step.city)
        self.__validate_step(self.__step)
        self.__last_city = self.__step.city
        self.__char = self.validate_char(self.__last_city)
        self.__city_used[self.__last_city] = self.__step.name
        self.__step = self.__new_step(self.__step)

    def __check_connect(self):
        if not self.__players:
            raise TypeError("Нету игроков")
        return True

    def __new_step(self, step: object) -> object:
        for player in self.__players:
            if player != step:
                new_step = player
                return new_step
    
    def __validate_step(self, step: object) -> bool:
        self.validate_city(step.city)
        player = self.__city_used.get(step.city, False)
        if player:
            raise TypeError(f"Этот город уже называл {player}")
        if self.__char:
            if self.__step.city[0] != self.__char:
                raise TypeError(f"Город должен начинаться на {self.__char.capitalize()}")

    def stop_game(self) -> str:
        winner = self.__step.name
        self.__disconnect(self.__players)
        return f"Игра остановлена, победил {winner}"

    def get_used_city(self) -> dict[str:str]:
        return self.__city_used

    @property
    def step(self) -> object:
        return self.__step

    @property
    def city_used(self):
        return self.__city_used

    @property
    def char(self) -> str:
        return self.__char

    @classmethod
    def validate_char(cls, city: str) -> str:
        '''
        Проверяет последнюю букву названия города
        Исключения ("Ъ", "ь", "ы", "й")
        Возвращает букву с которой может начинаться название города
        '''
        for char in city[::-1]:
            if char in cls.__wrong_char:
                continue
            else:
                break
        else:
            raise RuntimeError
        return char

    @classmethod
    def validate_city(cls, city: str) -> bool:
        if city not in cls.city_list:
            raise TypeError("Такого города нету")
        return True     

    @classmethod
    def form_list_city(cls, city_list: list) -> list:
        new_list = []
        for index in range(len(city_list)):
            city = cls.form_word_city(city_list[index])
            new_list.append(city)
        return new_list

    @staticmethod
    def form_word_city(city: str) -> str:
        '''
        Форматирует название города приводя к общему формату
        Убирает пробелы и интеры, заменяет 'ё' на 'е', 
                        переводит в ниж.регистр символы
        Возвращает отформатированное название города
        '''
        return city.strip().lower().replace('ё','е').replace('\n',"") 
    
    def __repr__(self) -> str:
        return f"<class: {self.__class__.__name__} attr: city_list - {type(self.city_list)!r}, players - {type(self.__players)!r}>"

class Player:
    def __init__(self, name: str, city: str | None = None, connect: GameCity | None = None) -> object:
        self.name = name
        self.connect = connect
        self.city = city

    def __repr__(self) -> str:
        return f"<class: {self.__class__.__name__} attr: name - {self.name!r}, city - {self.city!r}, game - {self.connect!r}>"
        
class Bot(Player):
    def __init__(self, name: str, city: str | None = None,  connect: GameCity | None = None) -> object:
        super().__init__(name, city, connect)

    def __step_bot(self) -> None:
        char = self.connect.char
        if char:
            for index in range(len(self.connect.city_list)):
                search_city = self.connect.city_used.get(self.connect.city_list[index], False)
                city = self.connect.city_list[index]
                if (not search_city) and (city[0] == char):
                    return city
            return None
        else:
            return self.random_city()
        
    @property
    def step(self):
        self.city = self.__step_bot()
        if self.city:
            return f"Город : {self.city.capitalize()}"
        self.connect.stop_game()
        return f"{self.name} проиграл"

    def random_city(self) -> str:
        '''
        Возвращает рандомный город из списка городов
        '''
        return choice(self.connect.city_list)  

with open("city.txt", "r", encoding='utf-8') as f:
    db_city = [city for city in f.readlines()]

formated_db_city = GameCity.form_list_city(db_city)

GameCity.city_list = formated_db_city

player_1 = Bot('Player')
player_2 = Bot('Bot')

players = [player_1, player_2]

game = GameCity(players)

def main():
    game.start()
    if game.step == player_1:
        print(player_1.step)
    if game.step == player_2:
        print(player_2.step)
    game.play()
    return main()

if __name__ == "__main__":
    main()