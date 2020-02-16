import threading
import time

from .directionairs.directionair import Directionair

from .direction import Direction
from .board import Board, GameOverException


def can_move_direction(
        previous_direction: Direction,
        next_direction: Direction,
) -> bool:
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


class Snake():

    def __init__(self, directionier: Directionair):
        self._directionier = directionier

    def get_new_direction(self, board) -> Direction:
        return self._directionier.get_new_direction(board)

    def get_direction(self) -> Direction:
        return self._directionier.get_direction()

    def set_direction(self, direction: Direction) -> None:
        self._directionier.set_direction(direction)

    def start(self) -> None:
        self._directionier.start()


class Game():

    def __init__(
            self,
            snake: Snake,
            board: Board,
            game_speed: float,
    ):
        self._round_count = 0
        self._game_speed = game_speed
        self._threading_event = threading.Event()
        self._snake = snake
        self._board = board

        self._game_over = False

    def _game_step(self) -> None:
        self._round_count += 1

    def _game_tick(self) -> None:
        print('_game_tick')
        tick_start_direction = self._snake.get_direction()
        time.sleep(self._game_speed)
        tick_current_direction = self._snake.get_new_direction(self._board)
        print(tick_current_direction)

        if can_move_direction(
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

    def start(self) -> None:
        self._snake.start()

        while not self._game_over:
            thread = threading.Thread(target=self._thread)
            thread.start()
            self._threading_event.wait()
            self._threading_event.clear()

    def get_game_summary(self) -> str:
        return f'Game over. Snake-length: {self._board.get_snake()} Steps: {self._round_count}'
