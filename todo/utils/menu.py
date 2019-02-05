import curses
import os
from collections import namedtuple

from todo.constants import INTERACTIVE_COMMANDS as COMMANDS
from todo.exceptions import TodoException
from todo.utils import strikethrough

X_OFFSET = 2
Y_OFFSET = 4
MARGIN = 2
NEXT_LINE = 1

NUMBER_OF_COMMANDS = 5


class Menu:
    __slots__ = ("stdscr", "color", "cols")

    commands = namedtuple(
        "Command",
        (
            COMMANDS.ADD,
            COMMANDS.DELETE,
            COMMANDS.DOWN,
            COMMANDS.EDIT,
            COMMANDS.ENTER,
            COMMANDS.ESCAPE,
            COMMANDS.QUIT,
            COMMANDS.RECOVER,
            COMMANDS.TOGGLE,
            COMMANDS.UP,
        ),
    )(
        add=(97,),
        delete=(100,),
        down=(curses.KEY_DOWN, 106),
        edit=(101,),
        enter=(10,),
        escape=(27,),
        quit=(113, 27),
        recover=(114,),
        toggle=(32,),
        up=(curses.KEY_UP, 107),
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
                self.blue = curses.color_pair(True)

                # add grey
                curses.init_pair(2, 8, -1)
                self.grey = curses.color_pair(2)
            except Exception:
                self.blue = 1
                self.grey = 1

    def __init__(self):
        os.environ.setdefault("ESCDELAY", "25")
        self.cols, _ = os.get_terminal_size()
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
        curses.curs_set(False)

    def _reset_screen(self):
        if hasattr(self, "stdscr"):
            # reverse the curses-friendly terminal settings
            self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()

        # restore the terminal to its original operating mode.
        curses.endwin()

    def _hellip_string(self, string, string_pos, cursor_pos, max_length):
        string_length = len(string)
        if string_length >= max_length:
            if string_pos >= cursor_pos:
                string = "…" + string[(string_pos - cursor_pos + 2):]

            leftovers = string_length - string_pos
            screen_space = max_length - cursor_pos
            if leftovers > screen_space:
                string = string[:max_length - 2] + "…"
        return string

    def _clear_commands(self, offset):
        # clear screen for commands
        for i in range(NUMBER_OF_COMMANDS):
            self.stdscr.move(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * (i + 2),
                0
            )
            self.clear_leftovers()

    def clear(self):
        # clear screen
        self.stdscr.clear()

    def clear_leftovers(self):
        # clear leftovers in line
        self.stdscr.clrtoeol()

    def refresh(self):
        self.stdscr.refresh()

    def get_command(self):
        command = self.stdscr.getch()
        if command in self.commands.add:
            return COMMANDS.ADD
        elif command in self.commands.delete:
            return COMMANDS.DELETE
        elif command in self.commands.down:
            return COMMANDS.DOWN
        elif command in self.commands.edit:
            return COMMANDS.EDIT
        elif command in self.commands.quit:
            return COMMANDS.QUIT
        elif command in self.commands.recover:
            return COMMANDS.RECOVER
        elif command in self.commands.toggle:
            return COMMANDS.TOGGLE
        elif command in self.commands.up:
            return COMMANDS.UP
        else:
            return None

    def render_header(self, text):
        self.stdscr.addstr(Y_OFFSET, X_OFFSET + MARGIN, text, curses.A_BOLD | self.color.blue)

    def render_subheader(self, text):
        self.stdscr.addstr(Y_OFFSET + NEXT_LINE, X_OFFSET + MARGIN, text)
        self.clear_leftovers()

    def render_todo(self, todo, offset, current_pos, is_deleted):
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

        # render empty state
        if is_deleted:
            self.stdscr.addstr(offset + Y_OFFSET + MARGIN + NEXT_LINE, X_OFFSET + MARGIN, " ")
        else:
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN + NEXT_LINE,
                X_OFFSET + MARGIN,
                "{completed}".format(completed="✓" if todo[3] else "x"),
                extra_style,
            )

        # render todo id
        todo_id_text = "{todo_id}".format(todo_id=todo[0])
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN + NEXT_LINE,
            X_OFFSET + MARGIN * 2,
            strikethrough(todo_id_text) if is_deleted else todo_id_text,
            curses.A_BOLD | extra_style,
        )

        # render todo name
        todo_name_text = "{name}".format(
            name=self._hellip_string(todo[1], 0, 1, self.cols - (X_OFFSET + MARGIN * 5 + 2))
        )
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN + NEXT_LINE,
            X_OFFSET + MARGIN * 5,
            ": {name}".format(name=strikethrough(todo_name_text) if is_deleted else todo_name_text),
            extra_style,
        )

        # clear leftovers
        self.clear_leftovers()

    def render_commands_for_edit_mode(self, offset):
        # clear screen for previous commands
        self._clear_commands(offset)

        # save
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE,
            X_OFFSET + MARGIN,
            "enter",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE,
            X_OFFSET + MARGIN * 5,
            "to save new title",
            self.color.grey,
        )

        # abort
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN,
            "escape",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN * 5,
            "to exit edit mode without saving",
            self.color.grey,
        )

    def render_commands(self, offset, is_deleted):
        # clear screen for previous commands
        self._clear_commands(offset)

        line_count = 1
        if is_deleted:
            # recover
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN,
                "r",
                curses.A_BOLD | self.color.grey,
            )
            self.clear_leftovers()
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN * 5,
                "to recover deleted todo",
                self.color.grey,
            )
            line_count += 1
        else:
            # add
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN,
                "a",
                curses.A_BOLD | self.color.grey,
            )
            self.clear_leftovers()
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN * 5,
                "to add a todo",
                self.color.grey,
            )
            line_count += 1

            # edit
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN,
                "e",
                curses.A_BOLD | self.color.grey,
            )
            self.clear_leftovers()
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN * 5,
                "to edit todo",
                self.color.grey,
            )
            line_count += 1

            # delete
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN,
                "d",
                curses.A_BOLD | self.color.grey,
            )
            self.clear_leftovers()
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN * 5,
                "to delete todo",
                self.color.grey,
            )
            line_count += 1

            # space
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN,
                "space",
                curses.A_BOLD | self.color.grey,
            )
            self.clear_leftovers()
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN * 5,
                "to toggle completed/uncompleted",
                self.color.grey,
            )
            line_count += 1

        # quit
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
            X_OFFSET + MARGIN,
            "q",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
            X_OFFSET + MARGIN * 5,
            "to quit",
            self.color.grey,
        )

    def edit_text(self, text, offset):
        Y_ORIGIN = offset + Y_OFFSET + MARGIN + NEXT_LINE
        X_ORIGIN = X_OFFSET + MARGIN * 5 + 2
        max_length = self.cols - X_ORIGIN

        # copy text
        string = text

        self.stdscr.addstr(
            Y_ORIGIN,
            X_ORIGIN,
            self._hellip_string(string, len(string), max_length, max_length),
            self.color.blue
        )
        self.clear_leftovers()
        self.refresh()
        try:
            # show cursor
            curses.curs_set(True)
            current_string_pos = len(string)
            y_pos, x_pos = self.stdscr.getyx()
            while True:
                string_length = len(string)
                relative_x_pos = x_pos - X_ORIGIN
                key = self.stdscr.getch()
                if key in self.commands.enter:
                    break
                elif key in self.commands.escape:
                    string = None
                    break
                elif key == curses.KEY_LEFT:
                    current_string_pos = max(current_string_pos - 1, 0)
                    if not (current_string_pos > 1 and relative_x_pos == 2):
                        x_pos = max(x_pos - 1, X_ORIGIN)
                elif key == curses.KEY_RIGHT:
                    current_string_pos = min(current_string_pos + 1, string_length)
                    if not(current_string_pos < string_length - 1 and relative_x_pos == max_length - 3):
                        x_pos = min(x_pos + 1, min(string_length + X_ORIGIN, self.cols - 1))
                elif key == 8 or key == 127 or key == curses.KEY_BACKSPACE:
                    if current_string_pos > 0:
                        string = string[:current_string_pos - 1] + string[current_string_pos:]
                        current_string_pos = max(current_string_pos - 1, 0)
                    if current_string_pos < x_pos - X_ORIGIN:
                        x_pos = max(x_pos - 1, X_ORIGIN)
                elif not curses.keyname(key).startswith(b"KEY_"):
                    string = string[:current_string_pos] + chr(key) + string[current_string_pos:]
                    current_string_pos = current_string_pos + 1
                    if not(current_string_pos < string_length - 1 and relative_x_pos == max_length - 3):
                        x_pos = min(x_pos + 1, self.cols - 1)

                # clear the line and rewrite string
                self.stdscr.move(y_pos, X_ORIGIN)
                self.clear_leftovers()
                self.stdscr.addstr(
                    Y_ORIGIN,
                    X_ORIGIN,
                    self._hellip_string(string, current_string_pos, x_pos - X_ORIGIN + 1, max_length),
                    self.color.blue,
                )

                # move cursor to correct place and refresh screen
                self.stdscr.move(y_pos, x_pos)
                self.stdscr.refresh()
        finally:
            curses.curs_set(False)
        return string
