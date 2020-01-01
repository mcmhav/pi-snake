import threading

from pynput import keyboard

from ..direction import Direction


class Keyboard():

    def __init__(self, init_direction=Direction.right):
        self._direction = init_direction

    def start(self):
        thread = threading.Thread(target=self._listen_for_direction)
        thread.start()

    def get_direction(self):
        return self._direction

    def get_new_direction(self):
        return self._direction

    def set_direction(self, direction: Direction):
        self._direction = direction

    def _listen_for_direction(self):
        print('_listen_for_direction')
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        try:
            if key == keyboard.Key.esc:
                # Stop listener
                return False
            # print('alphanumeric key {0} pressed'.format(key.char))
            if key.char == 'i':
                self.set_direction(Direction.up)
            elif key.char == 'k':
                self.set_direction(Direction.down)
            elif key.char == 'j':
                self.set_direction(Direction.left)
            elif key.char == 'l':
                self.set_direction(Direction.right)
        except AttributeError:
            # print('special key {0} pressed'.format(key))
            return
