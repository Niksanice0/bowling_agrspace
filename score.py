import argparse

from bowling import BowlingAPI


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Количство очков за матч')
    parser.add_argument('result', type=str, help='Результат матча')
    args = parser.parse_args()

    bowl = BowlingAPI(game_result=args.result)
    print(bowl.get_score())