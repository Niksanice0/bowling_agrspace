from collections import OrderedDict
from .Exceptions import ResultLong, InvalidSymbol, GameEnd


class BowlingAPI:
    _posible_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'x', '-', '/']

    def __init__(self, game_result):
        self.game_result = game_result
        self.total = 0
        self.game_data = OrderedDict({f'frame_{i}':
                                          {f'shot{y}':
                                               {'value': '',
                                                'close': False}
                                           for y in range(1, 3)}
                                      for i in range(1, 11)})

    def check_posible_value(self):
        if not isinstance(self.game_result, str):
            raise TypeError(f'Тип предоставленного результата неверный - {type(self.game_result)}')
        if len(self.game_result) > 20:
            raise ResultLong(f'Длина представленного результата превышена - {len(self.game_result)}')
        for value in self.game_result:
            self.game_result.lower()
            if value not in self._posible_values:
                raise ValueError(f'В результатах игры найдено некорректное значение - {value}')

    def get_score(self):
        # получить счет
        self.check_posible_value()
        for symbol in self.game_result:
            self.check_symbol(symbol)
        return f'Количество очков для результатов {self.game_result} - {self.total}'

    def check_symbol(self, symbol):
        for frame in self.game_data.values():
            self.check_data()
            for number, shots in enumerate(frame.values(), 1):
                if shots['close'] is False:
                    if number == 1 and symbol in self._posible_values:
                        self.first_shot(symbol=symbol, frame=frame)
                    elif number == 2 and symbol in self._posible_values[:-1]:
                        self.second_shot(symbol=symbol, frame=frame)
                    shots['value'] = symbol
                    shots['close'] = True
                    return
                else:
                    continue

    def first_shot(self, symbol, frame):
        if symbol == 'x':
            self.close_frame(frame)
            self.total += 20
        if symbol in [str(i) for i in range(1, 10)]:
            self.total += int(symbol)
        if symbol == '/':
            raise InvalidSymbol(f'{symbol} не может быть использован для первого броска')
        return

    def second_shot(self, symbol, frame):
        if symbol == 'x':
            if frame['shot1']['value'] == '-':
                self.total += 20
            else:
                raise ValueError(f'{symbol} не может быть использован для второго броска в данном случае, т.к. '
                                 f'результатом первого броска является - {frame["shot1"]["value"]}')
        if symbol in [str(i) for i in range(1, 10)]:
            if frame['shot1']['value'] in [str(i) for i in range(1, 10)]:
                if int(symbol) + int(frame['shot1']['value']) < 10:
                    self.total += int(symbol)
                else:
                    raise ValueError(f'Превышено значение сбитых кегль за фрейм')
            elif frame['shot1']['value'] == '-':
                self.total += int(symbol)
            else:
                raise ValueError(f'Неверный символ для второго броска - {symbol}')
        if symbol == '/':
            if frame['shot1']['value'] in [str(i) for i in range(1, 10)]:
                self.total += 10 - int(frame['shot1']['value'])
            else:
                raise ValueError(f'Неверный символ для второго броска - {symbol}')
        return

    def close_frame(self, frame):
        # закончить фрейм игры
        for number, shots in enumerate(frame.values(), 1):
            if number == 2:
                shots['close'] = True

    def check_data(self):
        # проверка на заполненность результатов
        values = []
        for shots in self.game_data.values():
            for shot in shots.values():
                values.append(shot['close'])
        if all(values):
            raise GameEnd('Все фреймы заполнены. Конец игры')
