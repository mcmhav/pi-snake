import argparse

from pi_snake.directionairs.directionair import Directionair
from pi_snake.drawers import Pihat, Sysout
from pi_snake.pi_snake import Board, Game, Snake

parser = argparse.ArgumentParser(description='pi-snake.')
parser.add_argument(
    '--drawer',
    dest='drawer',
    default='sysout',
    help='Drawer for the game',
)
parser.add_argument(
    '--directionier',
    dest='directionier',
    default='sysout',
    help='Dictionair for the game',
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

ARGS = parser.parse_args()


def main(args) -> None:
    print('Starting game')
    print(args.drawer)
    print(args.size)
    print(args.game_speed)
    drawer = None
    if args.drawer == 'sense_hat':
        drawer = Pihat()
    else:
        drawer = Sysout()

    directionier: Directionair
    if args.directionier == 'keyboard':
        from pi_snake.directionairs.keyboard import Keyboard
        directionier = Keyboard()
    elif args.directionier == 'crash_avoider':
        from pi_snake.directionairs.crash_avoider import CrashAvoider
        directionier = CrashAvoider()
    elif args.directionier == 'horizontal':
        from pi_snake.directionairs.horizontal import Horizontal
        directionier = Horizontal()
    else:
        from pi_snake.directionairs.random import Random
        directionier = Random()

    snake = Snake(directionier)
    board = Board(drawer=drawer, size=args.size)
    game = Game(snake, board, game_speed=args.game_speed)
    try:
        game.start()
    except Exception as e:
        print('error', e)
    finally:
        drawer.clear(game.get_game_summary())


if __name__ == '__main__':
    main(ARGS)
