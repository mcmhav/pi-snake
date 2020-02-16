import random

from pi_snake.board import Board

from ..direction import Direction
from .directionair import Directionair

DIRECTIONS = {
    0: Direction.right,
    1: Direction.up,
}


class Horizontal(Directionair):

    def __init__(
            self,
            init_direction: Direction = Direction.right,
            seed: int = 1,
    ):
        super().__init__(init_direction)
        self._seed = seed

    def get_new_direction(self, board: Board) -> Direction:
        new_direction = Direction.right
        if len(board._snake) > board._size:
            movement = board.direction_to_movement(Direction.right)
            if board._board[movement[0]][movement[1]] == 's':
                new_direction = Direction.up
        else:
            new_direction = DIRECTIONS[random.randint(0, 1)]
        self._direction = new_direction
        return new_direction
