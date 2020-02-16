import math
import random
from typing import List

from .direction import Direction
from .drawers.drawer import Drawer


class GameOverException(Exception):

    def __init__(self, message):
        self.message = message


class Board():

    def __init__(
            self,
            drawer: Drawer,
            size: int = 5,
    ):
        self._size = size
        self._board = self._init_board()
        self._snake = [[
            math.floor(self._size / 2),
            math.floor(self._size / 2) - 2,
        ], [
            math.floor(self._size / 2),
            math.floor(self._size / 2) - 1,
        ], [
            math.floor(self._size / 2),
            math.floor(self._size / 2),
        ]]
        self._init_snake()
        self._place_apple()
        self._drawer = drawer

    def _init_board(self) -> List:
        return [[''] * self._size for i in range(self._size)]

    def _init_snake(self) -> None:
        self._update_snake()

    def _update_tile(self, tile: List, value: str) -> None:
        self._board[tile[0]][tile[1]] = value

    def _update_snake(self) -> None:
        for snake_block in self._snake:
            self._update_tile(snake_block, 's')

    def _can_place_apple(self, apple: List) -> bool:
        return self._board[apple[0]][apple[1]] == ''

    def _place_apple(self) -> None:
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

    def move_snake(self, direction: Direction) -> None:
        movement = self.direction_to_movement(direction)
        self._snake.append(movement)

        if (len(self._snake) + 1) == self._size * self._size:
            raise GameOverException('Game won! :)')
        if self._board[self._snake[-1][0]][self._snake[-1][1]] == '':
            self._update_tile(self._snake[0], '')
            self._snake.pop(0)
        elif self._board[self._snake[-1][0]][self._snake[-1][1]] == 's':
            raise GameOverException('game over! :(')
        elif self._board[self._snake[-1][0]][self._snake[-1][1]] == 'g':
            self._place_apple()

        self._update_snake()

    def direction_to_movement(self, direction: Direction) -> List:
        movement = None
        if direction == Direction.up:
            movement = [
                (self._snake[-1][0] - (1 % self._size)) % self._size,
                self._snake[-1][1],
            ]
        elif direction == Direction.right:
            movement = [
                self._snake[-1][0],
                (self._snake[-1][1] + (1 % self._size)) % self._size,
            ]
        elif direction == Direction.down:
            movement = [
                (self._snake[-1][0] + (1 % self._size)) % self._size,
                self._snake[-1][1],
            ]
        elif direction == Direction.left:
            movement = [
                self._snake[-1][0],
                (self._snake[-1][1] - (1 % self._size)) % self._size,
            ]
        else:
            raise ValueError('Not valid direction')

        return movement

    def draw(self) -> None:
        self._drawer.draw(self._board)

    def get_snake(self) -> List:
        return self._snake
