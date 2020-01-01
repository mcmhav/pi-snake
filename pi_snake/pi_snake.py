import math
import random
import threading
import time

import pi_snake.directionairs as directionairs

from .direction import Direction


class GameOverException(Exception):
    pass


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
        self._snake = [[
            math.floor(self._size / 2),
            math.floor(self._size / 2),
        ], [
            math.floor(self._size / 2),
            math.floor(self._size / 2) - 1,
        ], [
            math.floor(self._size / 2),
            math.floor(self._size / 2) - 2,
        ]]
        self._init_snake()
        self._place_apple()
        self._drawer = drawer

    def _init_board(self):
        return [[''] * self._size for i in range(self._size)]

    def _init_snake(self):
        self._update_snake()

    def _update_tile(self, tile, value):
        self._board[tile[0]][tile[1]] = value

    def _update_snake(self):
        for snake_block in self._snake:
            self._update_tile(snake_block, 's')

    def _can_place_apple(self, apple):
        return self._board[apple[0]][apple[1]] == ''

    def _place_apple(self):
        apple = [
            random.randint(0, self._size - 1),
            random.randint(0, self._size - 1),
        ]
        while not self._can_place_apple(apple):
            apple = [
                random.randint(0, self._size - 1),
                random.randint(0, self._size - 1),
            ]

        self._update_tile(apple, 'g')

    def move_snake(self, direction):
        if direction == Direction.up:
            self._snake.append([
                (self._snake[-1][0] - (1 % self._size)) % self._size,
                self._snake[-1][1],
            ])
        elif direction == Direction.right:
            self._snake.append([
                self._snake[-1][0],
                (self._snake[-1][1] + (1 % self._size)) % self._size,
            ])
        elif direction == Direction.down:
            self._snake.append([
                (self._snake[-1][0] + (1 % self._size)) % self._size,
                self._snake[-1][1],
            ])
        elif direction == Direction.left:
            self._snake.append([
                self._snake[-1][0],
                (self._snake[-1][1] - (1 % self._size)) % self._size,
            ])

        if self._board[self._snake[-1][0]][self._snake[-1][1]] == '':
            self._update_tile(self._snake[0], '')
            self._snake.pop(0)
        elif self._board[self._snake[-1][0]][self._snake[-1][1]] == 's':
            print('game over')
            raise GameOverException('game over')
        elif self._board[self._snake[-1][0]][self._snake[-1][1]] == 'g':
            self._place_apple()

        self._update_snake()

    def draw(self):
        self._drawer.draw(self._board)


class Game():

    def __init__(self, snake, board, game_speed):
        self._round_count = 0
        self._game_speed = game_speed
        self._threading_event = threading.Event()
        self._snake = snake
        self._board = board

        self._game_over = False

    def _game_step(self):
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

        self._game_step()

        self._board.draw()

    def _thread(self):
        try:
            self._game_tick()
        except GameOverException as e:
            print('=' * 10)
            self._game_over = True

        self._threading_event.set()

    def start(self):
        self._snake.start()

        while not self._game_over:
            thread = threading.Thread(target=self._thread)
            thread.start()
            self._threading_event.wait()
            self._threading_event.clear()

    def get_game_summary(self):
        return f'Game steps: {self._round_count}'
