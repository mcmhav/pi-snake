import argparse
from pi_snake.drawers import Sysout, Pihat

from pi_snake.pi_snake import Snake, Board, Game
import pi_snake.directionairs as directionairs

parser = argparse.ArgumentParser(description='pi-snake.')
parser.add_argument(
    '--drawer',
    dest='drawer',
    default='sysout',
    help='Drawer for the game',
)
parser.add_argument(
    '--size',
    dest='size',
    default=8,
    help='Size of the board',
    type=int,
)
parser.add_argument(
    '--game-speed',
    dest='game_speed',
    default=0.5,
    help='Speed of the game',
    type=float,
)

args = parser.parse_args()


def main() -> None:
    print('Starting game')
    print(args.drawer)
    print(args.size)
    print(args.game_speed)
    drawer = None
    if args.drawer == 'sense_hat':
        from sense_hat import SenseHat
        sense = SenseHat()
        drawer = Pihat(sense)
    else:
        drawer = Sysout()

    snake = Snake(directionairs.Random())
    board = Board(drawer=drawer, size=args.size)
    game = Game(snake, board, game_speed=args.game_speed)
    try:
        game.start()
    finally:
        drawer.clear()


if __name__ == '__main__':
    main()
