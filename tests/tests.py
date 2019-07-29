# -*- coding: utf-8 -*-
import unittest
from collections import OrderedDict

from lesson_014.bowling import BowlingAPI
from lesson_014.Exceptions import ResultLong, InvalidSymbol, GameEnd


# на винде не работает from ..


class BowlingAPITest(unittest.TestCase):
    def setUp(self):
        self.game_result = 'xxxxx'
        self.total = 0
        self.bowling_api = BowlingAPI(self.game_result)
        self.game_data = OrderedDict({'frame_1':
                                          {'shot1': {'close': True, 'value': ''},
                                           'shot2': {'close': False, 'value': ''}}})

    def test_type_result(self):
        self.assertEqual(self.bowling_api.check_posible_value(), None)
        self.bowling_api.game_result = list()
        self.assertRaises(TypeError, self.bowling_api.check_posible_value, )

    def test_len_result(self):
        self.assertEqual(self.bowling_api.check_posible_value(), None)
        self.bowling_api.game_result = '1' * 21
        self.assertRaises(ResultLong, self.bowling_api.check_posible_value, )

    def test_value_result(self):
        self.assertEqual(self.bowling_api.check_posible_value(), None)
        self.bowling_api.game_result = 'X123/R'
        self.assertRaises(ValueError, self.bowling_api.check_posible_value, )

    def test_close_frame(self):
        self.bowling_api.close_frame(frame=self.game_data['frame_1'])
        self.assertEqual(self.game_data['frame_1']['shot2']['close'], True)

    def test_check_data(self):
        self.assertEqual(self.bowling_api.check_data(), None)

    def test_check_data_exc(self):
        self.game_data = OrderedDict({'frame_1':
                                          {'shot1': {'close': True, 'value': '-'},
                                           'shot2': {'close': True, 'value': ''}}})
        self.assertRaises(GameEnd, self.bowling_api.check_data(), )

    def test_first_shot_symbol_x(self):
        self.bowling_api.first_shot(symbol='x', frame=self.game_data['frame_1'])
        self.assertEqual(self.bowling_api.total, 20)

    def test_first_shot_symbol_digit(self):
        for digit in range(1, 10):
            self.bowling_api.total = 0
            self.bowling_api.first_shot(symbol=str(digit), frame=self.game_data['frame_1'])
            self.assertEqual(self.bowling_api.total, digit)

    def test_first_shot_symbol_slash(self):
        self.assertRaises(InvalidSymbol, self.bowling_api.first_shot, '/', self.game_data['frame_1'])

    def test_second_shot_symbol_x(self):
        self.game_data = OrderedDict({'frame_1':
                                          {'shot1': {'close': True, 'value': '-'},
                                           'shot2': {'close': False, 'value': ''}}})
        self.bowling_api.first_shot(symbol='x', frame=self.game_data['frame_1'])
        self.assertEqual(self.bowling_api.total, 20)

    def test_second_shot_symbol_x_exception(self):
        self.assertRaises(ValueError, self.bowling_api.second_shot, 'x', self.game_data['frame_1'])

    def test_second_shot_symbol_slash(self):
        for i in range(1, 10):
            self.bowling_api.total = 0
            self.game_data['frame_1']['shot1']['value'] = str(i)
            self.bowling_api.second_shot(symbol='/', frame=self.game_data['frame_1'])
            self.assertEqual(self.bowling_api.total, 10 - int(self.game_data['frame_1']['shot1']['value']))

    def test_second_shot_symbol_slash_exception(self):
        self.game_data = OrderedDict({'frame_1':
                                          {'shot1': {'close': True, 'value': 'x'},
                                           'shot2': {'close': False, 'value': ''}}})
        self.assertRaises(ValueError, self.bowling_api.second_shot, '/', self.game_data['frame_1'])

    def test_second_shot_symbol_digit(self):
        self.game_data['frame_1']['shot1']['value'] = '-'
        for i in range(1, 10):
            self.bowling_api.total = 0
            self.bowling_api.second_shot(symbol=str(i), frame=self.game_data['frame_1'])
            self.assertEqual(self.bowling_api.total, i)
        for i in range(1, 10):
            self.game_data['frame_1']['shot1']['value'] = str(i)
            self.bowling_api.total = 0
            if i * 2 >= 10:
                self.assertRaises(ValueError, self.bowling_api.second_shot, str(i), self.game_data['frame_1'])
            else:
                self.bowling_api.second_shot(symbol=str(i), frame=self.game_data['frame_1'])
                self.assertEqual(self.bowling_api.total, int(i))


if __name__ == '__main__':
    unittest.main()
