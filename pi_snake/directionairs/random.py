from ..direction import Direction
import random

DIRECTIONS = {
    0: Direction.right,
    1: Direction.up,
    2: Direction.down,
    3: Direction.left,
}


class Random():

    def __init__(self, init_direction=Direction.right, seed=1):
        self._seed = seed
        self._direction = init_direction

    def start(self):
        return

    def set_direction(self, direction):
        self._direction = direction

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

    def get_direction(self):
        return self._direction

    def get_new_direction(self):
        new_direction = DIRECTIONS[random.randint(0, 3)]
        while not self._can_move_direction(self._direction, new_direction):
            new_direction = DIRECTIONS[random.randint(0, 3)]
        self._direction = new_direction
        return new_direction
