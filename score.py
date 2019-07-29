import argparse

from bowling import BowlingAPI


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='��������� ����� �� ����')
    parser.add_argument('result', type=str, help='��������� �����')
    args = parser.parse_args()

    bowl = BowlingAPI(game_result=args.result)
    print(bowl.get_score())