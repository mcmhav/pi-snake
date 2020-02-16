from ..direction import Direction

from .random import Random, DIRECTIONS

from pi_snake.board import Board

DIRECTIONS = {
    0: Direction.right,
    1: Direction.up,
    2: Direction.down,
    3: Direction.left,
}


class CrashAvoider(Random):

    def get_new_direction(self, board: Board) -> Direction:
        new_direction = None
        retries = 0
        while not new_direction:
            new_direction = super().get_new_direction(board)

            movement = board.direction_to_movement(new_direction)
            if board._board[movement[0]][movement[1]] == 's' and retries < 10:
                new_direction = None
                retries += 1
                print('retries:', retries)

        return new_direction
