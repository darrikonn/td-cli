from todo.utils import hellip_postfix, hellip_prefix


class HorizontalTracker:
    __slots__ = ("_string", "_string_pos", "_cursor_pos", "_x_origin", "_terminal_width")

    def __init__(self, string, x_origin, terminal_width):
        string_length = len(string)

        self._string = string
        self._string_pos = string_length
        self._cursor_pos = min(terminal_width - 1, string_length + x_origin)
        self._x_origin = x_origin
        self._terminal_width = terminal_width

    @property
    def _relative_cursor_pos(self):
        return self._cursor_pos - self._x_origin

    @property
    def _max_length(self):
        return self._terminal_width - self._x_origin

    @property
    def _string_length(self):
        return len(self._string)

    def move_left(self):
        self._string_pos = max(self._string_pos - 1, 0)
        if not (self._string_pos > 1 and self._relative_cursor_pos == 2):
            self._cursor_pos = max(self._cursor_pos - 1, self._x_origin)

    def move_right(self):
        self._string_pos = min(self._string_pos + 1, self._string_length)
        if not (
            self._string_pos < self._string_length - 1
            and self._relative_cursor_pos == self._max_length - 3
        ):
            self._cursor_pos = min(
                self._cursor_pos + 1,
                min(self._string_length + self._x_origin, self._terminal_width - 1),
            )

    def move_to_start(self):
        self._string_pos = 0
        self._cursor_pos = self._x_origin

    def move_to_end(self):
        self._string_pos = self._string_length
        self._cursor_pos = min(self._string_length + self._x_origin, self._terminal_width - 1)

    def delete(self):
        if self._string_pos > 0:
            self._string = self._string[: self._string_pos - 1] + self._string[self._string_pos :]
            self._string_pos = max(self._string_pos - 1, 0)
        if self._string_pos < self._relative_cursor_pos:
            self._cursor_pos = max(self._cursor_pos - 1, self._x_origin)

    def delete_backwards(self):
        if self._string_pos < self._string_length:
            self._string = self._string[: self._string_pos] + self._string[self._string_pos + 1 :]
        if self._string_pos > self._relative_cursor_pos:
            self._cursor_pos = min(self._cursor_pos + 1, self._terminal_width - 1)

    def add(self, char):
        self._string = self._string[: self._string_pos] + char + self._string[self._string_pos :]
        self._string_pos = self._string_pos + 1
        if not (
            self._string_pos < self._string_length - 1
            and self._relative_cursor_pos == self._max_length - 3
        ):
            self._cursor_pos = min(self._cursor_pos + 1, self._terminal_width - 1)

    def erase_string(self):
        self._string = None

    def get_hellip_string(self):
        # make a copy
        string = self._string
        if self._string_length >= self._max_length:
            if self._string_pos > self._relative_cursor_pos:
                string = hellip_prefix(string, self._string_pos - self._relative_cursor_pos + 1)

            leftovers = self._string_length - self._string_pos
            screen_space = self._max_length - self._relative_cursor_pos
            if leftovers >= screen_space:
                string = hellip_postfix(string, self._max_length - 2)
        return string

    def get_string(self):
        return self._string

    def get_cursor_pos(self):
        return self._cursor_pos
