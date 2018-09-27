import curses
from collections import namedtuple

from todo.constants import INTERACTIVE_COMMANDS as COMMANDS
from todo.exceptions import TodoException

X_OFFSET = 2
Y_OFFSET = 4
MARGIN = 2
NEXT_LINE = 1


class Menu:
    __slots__ = ("stdscr", "color")

    commands = namedtuple("Command", (COMMANDS.DOWN, COMMANDS.UP, COMMANDS.TOGGLE, COMMANDS.QUIT))(
        down=(curses.KEY_DOWN, 106), up=(curses.KEY_UP, 107), toggle=(32,), quit=(113, 27)
    )

    class Color:
        __slots__ = ("blue", "grey")

        def __init__(self):
            try:
                # init colors
                curses.start_color()
                curses.use_default_colors()

                # add blue
                curses.init_pair(1, curses.COLOR_BLUE, -1)
                self.blue = curses.color_pair(1)

                # add grey
                curses.init_pair(2, 8, -1)
                self.grey = curses.color_pair(2)
            except Exception:
                self.blue = 1
                self.grey = 1

    def __init__(self):
        self.stdscr = curses.initscr()
        try:
            self._setup_screen()
        except Exception as e:
            self._reset_screen()
            raise TodoException("Error occurred, could not initialize menu", e)
        self.color = self.Color()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._reset_screen()

        if exc_type is not None:
            return False
        return True

    def _setup_screen(self):
        # turn off automatic echoing of keys to the screen
        curses.noecho()

        # react to keys instantly, without requiring the Enter key to be pressed
        curses.cbreak()

        # enable return of special keys
        self.stdscr.keypad(True)

        # remove curser
        curses.curs_set(0)

    def _reset_screen(self):
        if hasattr(self, "stdscr"):
            # reverse the curses-friendly terminal settings
            self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()

        # restore the terminal to its original operating mode.
        curses.endwin()

    def clear(self):
        # clear screen
        self.stdscr.clear()

    def refresh(self):
        self.stdscr.refresh()

    def get_command(self):
        command = self.stdscr.getch()
        if command in self.commands.down:
            return COMMANDS.DOWN
        elif command in self.commands.up:
            return COMMANDS.UP
        elif command in self.commands.toggle:
            return COMMANDS.TOGGLE
        elif command in self.commands.quit:
            return COMMANDS.QUIT
        else:
            return None

    def render_header(self, text):
        self.stdscr.addstr(Y_OFFSET, X_OFFSET + MARGIN, text, curses.A_BOLD | self.color.blue)

    def render_subheader(self, text):
        self.stdscr.addstr(Y_OFFSET + NEXT_LINE, X_OFFSET + MARGIN, text)

    def render_todo(self, todo, offset, current_pos):
        extra_style = 1
        if offset == current_pos:
            extra_style = self.color.blue
            # render active cursor
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN + NEXT_LINE,
                X_OFFSET,
                "❯",
                curses.A_BOLD | self.color.blue,
            )
        else:
            # render non-active cursor
            self.stdscr.addstr(offset + Y_OFFSET + MARGIN + NEXT_LINE, X_OFFSET, " ")

        # render completed
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN + NEXT_LINE,
            X_OFFSET + MARGIN,
            "{completed}".format(completed="✓" if todo[3] else "x"),
            extra_style,
        )
        # render todo id
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN + NEXT_LINE,
            X_OFFSET + MARGIN * 2,
            "{todo_id}".format(todo_id=todo[0]),
            curses.A_BOLD | extra_style,
        )
        # render todo name
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN + NEXT_LINE,
            X_OFFSET + MARGIN * 5,
            ": {name}".format(name=todo[1]),
            extra_style,
        )

    def render_commands(self, offset):
        # space
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE,
            X_OFFSET + MARGIN,
            "space",
            curses.A_BOLD | self.color.grey,
        )
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE,
            X_OFFSET + MARGIN * 5,
            "to toggle completed/uncompleted",
            self.color.grey,
        )

        # quit
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN,
            "q",
            curses.A_BOLD | self.color.grey,
        )
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN * 5,
            "to quit",
            self.color.grey,
        )
