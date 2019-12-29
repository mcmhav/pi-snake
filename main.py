import enum
import math
from drawers.pi_draw import Pihat


class Direction(enum.Enum):
    up = 'UP'
    right = 'RIGHT'
    left = 'LEFT'
    down = 'DOWN'


class Snake():

    def __init__(self):
        self._direction = Direction.right

    def _set_direction(self, direction) -> None:
        self._direction = direction

    def listen_for_direction(self):
        print('listen_for_direction')
        from pynput import keyboard
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        try:
            if key == keyboard.Key.esc:
                # Stop listener
                return False
            # print('alphanumeric key {0} pressed'.format(key.char))
            if key.char == 'i':
                self._set_direction(Direction.up)
            elif key.char == 'k':
                self._set_direction(Direction.down)
            elif key.char == 'j':
                self._set_direction(Direction.left)
            elif key.char == 'l':
                self._set_direction(Direction.right)
        except AttributeError:
            # print('special key {0} pressed'.format(key))
            return


class Sysout():

    @staticmethod
    def draw(board):
        for row in board:
            print(row)


class Board():

    def __init__(self, size=5, drawer=Sysout()):
        self._size = size
        self._board = self._init_board()
        self._snake_head = [
            math.floor(self._size / 2),
            math.floor(self._size / 2),
        ]
        self._init_snake()
        self._drawer = drawer

    def _init_board(self):
        return [[''] * self._size for i in range(self._size)]

    def _init_snake(self):
        print(self._board)
        self._update_tile(self._snake_head, 's')

    def _update_tile(self, tile, value):
        self._board[tile[0]][tile[1]] = value

    def move_snake(self, direction):
        self._update_tile(self._snake_head, '')
        if direction == Direction.up:
            self._snake_head[0] -= (1 % self._size)
            self._snake_head[0] = (self._snake_head[0] % self._size)
        elif direction == Direction.right:
            self._snake_head[1] += (1 % self._size)
            self._snake_head[1] = (self._snake_head[1] % self._size)
        elif direction == Direction.down:
            self._snake_head[0] += (1 % self._size)
            self._snake_head[0] = (self._snake_head[0] % self._size)
        elif direction == Direction.left:
            self._snake_head[1] -= (1 % self._size)
            self._snake_head[1] = (self._snake_head[1] % self._size)

        self._update_tile(self._snake_head, 's')

    def draw(self):
        self._drawer.draw(self._board)


import threading
import time


class Game():

    def __init__(self, snake, board, game_speed=1):
        self._round_count = 0
        self._game_speed = game_speed
        self._threading_event = threading.Event()
        self._snake = snake
        self._board = board

    def game_step(self):
        self._round_count += 1

    def _can_move_direction(self, previous_direction, next_direction):
        if ((previous_direction == Direction.up
             and next_direction == Direction.down)
                or (previous_direction == Direction.down
                    and next_direction == Direction.up)
                or (previous_direction == Direction.right
                    and next_direction == Direction.left)
                or (previous_direction == Direction.left
                    and next_direction == Direction.right)):
            return False
        return True

    def _game_tick(self):
        print('_game_tick')
        tick_start_direction = self._snake._direction
        time.sleep(self._game_speed)
        tick_current_direction = self._snake._direction
        print(tick_current_direction)

        if self._can_move_direction(
                tick_start_direction,
                tick_current_direction,
        ):
            self._board.move_snake(tick_current_direction)
        else:
            self._board.move_snake(tick_start_direction)
            self._snake._set_direction(tick_start_direction)

        self._board.draw()
        self._threading_event.set()

    def start(self):

        thread_2 = threading.Thread(target=self._snake.listen_for_direction)
        thread_2.start()
        while True:
            print('Game tick')
            thread = threading.Thread(target=self._game_tick)
            thread.start()
            self._threading_event.wait()
            self._threading_event.clear()


def main() -> None:
    print('Starting game')
    from sense_hat import SenseHat
    sense = SenseHat()
    snake = Snake()
    board = Board(size=8, drawer=Pihat(sense))
    game = Game(snake, board, game_speed=0.5)
    try:
        game.start()
        # snake.listen_for_direction()
    finally:
        sense.close()


if __name__ == '__main__':
    main()
