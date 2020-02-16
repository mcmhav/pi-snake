from pi_snake.board import Board

from ..direction import Direction
from .random import DIRECTIONS, Random


class CrashAvoider(Random):

    def get_new_direction(self, board: Board) -> Direction:
        new_direction = None
        retries = 0
        while not new_direction:
            new_direction = super().get_new_direction(board)

            movement = board.direction_to_movement(new_direction)
            if board._board[movement[0]][movement[1]] == 's' and retries < 10:
                print('retries:', retries, 'tried going:', new_direction)
                new_direction = None
                retries += 1

        return new_direction
