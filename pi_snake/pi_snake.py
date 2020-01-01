import enum
import math
import random
import threading
import time

import pi_snake.directionairs as directionairs

from .direction import Direction


class Snake():

    def __init__(self, directionier):
        self._directionier = directionier

    def get_new_direction(self):
        return self._directionier.get_new_direction()

    def get_direction(self):
        return self._directionier.get_direction()

    def set_direction(self, direction):
        self._directionier.set_direction(direction)

    def start(self):
        self._directionier.start()


class Board():

    def __init__(
            self,
            drawer,
            size=5,
    ):
        self._size = size
        self._board = self._init_board()
        self._snake_head = [
            math.floor(self._size / 2),
            math.floor(self._size / 2),
        ]
        self._apple = [
            random.randint(0, size - 1),
            random.randint(0, size - 1),
        ]
        self._init_apple()
        self._init_snake()
        self._drawer = drawer

    def _init_board(self):
        return [[''] * self._size for i in range(self._size)]

    def _init_snake(self):
        print(self._board)
        self._update_tile(self._snake_head, 's')

    def _init_apple(self):
        self._update_tile(self._apple, 'g')

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


class Game():

    def __init__(self, snake, board, game_speed):
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
        tick_start_direction = self._snake.get_direction()
        time.sleep(self._game_speed)
        tick_current_direction = self._snake.get_new_direction()
        print(tick_current_direction)

        if self._can_move_direction(
                tick_start_direction,
                tick_current_direction,
        ):
            self._board.move_snake(tick_current_direction)
        else:
            self._board.move_snake(tick_start_direction)
            self._snake.set_direction(tick_start_direction)

        self._board.draw()
        self._threading_event.set()

    def start(self):

        self._snake.start()

        while True:
            thread = threading.Thread(target=self._game_tick)
            thread.start()
            self._threading_event.wait()
            self._threading_event.clear()
