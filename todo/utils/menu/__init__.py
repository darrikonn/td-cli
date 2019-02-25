import curses
import os
from collections import namedtuple

from todo.constants import COMMAND_MODES
from todo.constants import INTERACTIVE_COMMANDS as COMMANDS
from todo.exceptions import TodoException
from todo.utils import strikethrough, hellip_postfix

from .horizontal_tracker import HorizontalTracker

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

    def _clear_commands(self, offset, number_of_commands=NUMBER_OF_COMMANDS):
        # clear screen for commands
        for i in range(number_of_commands):
            self.stdscr.move(offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * (i + 2), 0)
            self.clear_leftovers()

    def _render_add_commands(self, offset):
        # clear screen for previous commands
        self._clear_commands(offset - 2, NUMBER_OF_COMMANDS + 1)

        # save
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 1,
            X_OFFSET + MARGIN,
            "enter",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 1,
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

    def _render_edit_commands(self, offset):
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

    def _render_empty_commands(self, offset):
        # clear screen for previous commands
        self._clear_commands(offset)

        # add
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 1,
            X_OFFSET + MARGIN,
            "a",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 1,
            X_OFFSET + MARGIN * 5,
            "to add a todo",
            self.color.grey,
        )

        # quit
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN,
            "q",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN * 5,
            "to quit",
            self.color.grey,
        )

    def _render_delete_commands(self, offset):
        # clear screen for previous commands
        self._clear_commands(offset)

        # add
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 1,
            X_OFFSET + MARGIN,
            "a",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 1,
            X_OFFSET + MARGIN * 5,
            "to add a todo",
            self.color.grey,
        )

        # recover
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN,
            "r",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN * 5,
            "to recover deleted todo",
            self.color.grey,
        )

        # quit
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 3,
            X_OFFSET + MARGIN,
            "q",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 3,
            X_OFFSET + MARGIN * 5,
            "to quit",
            self.color.grey,
        )

    def _render_default_commands(self, offset):
        # clear screen for previous commands
        self._clear_commands(offset)

        # add
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 1,
            X_OFFSET + MARGIN,
            "a",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 1,
            X_OFFSET + MARGIN * 5,
            "to add a todo",
            self.color.grey,
        )

        # edit
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN,
            "e",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN * 5,
            "to edit todo",
            self.color.grey,
        )

        # delete
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 3,
            X_OFFSET + MARGIN,
            "d",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 3,
            X_OFFSET + MARGIN * 5,
            "to delete todo",
            self.color.grey,
        )

        # space
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 4,
            X_OFFSET + MARGIN,
            "space",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 4,
            X_OFFSET + MARGIN * 5,
            "to toggle completed/uncompleted",
            self.color.grey,
        )

        # quit
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 5,
            X_OFFSET + MARGIN,
            "q",
            curses.A_BOLD | self.color.grey,
        )
        self.clear_leftovers()
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 5,
            X_OFFSET + MARGIN * 5,
            "to quit",
            self.color.grey,
        )

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

        if is_deleted or todo[3] is None:
            # render empty state
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
        screen_space = self.cols - (X_OFFSET + MARGIN * 5 + 4)
        name_length = len(todo[1])
        todo_name_text = "{name}".format(
            name=hellip_postfix(todo[1], screen_space) if name_length > screen_space else todo[1]
        )
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN + NEXT_LINE,
            X_OFFSET + MARGIN * 5,
            ": {name}".format(name=strikethrough(todo_name_text) if is_deleted else todo_name_text),
            extra_style,
        )

        # clear leftovers
        self.clear_leftovers()

    def render_commands(self, offset, mode=COMMAND_MODES.DEFAULT):
        if mode == COMMAND_MODES.ADD:
            self._render_add_commands(offset)
        elif mode == COMMAND_MODES.EMPTY:
            self._render_empty_commands(offset)
        elif mode == COMMAND_MODES.DEFAULT:
            self._render_default_commands(offset)
        elif mode == COMMAND_MODES.DELETE:
            self._render_delete_commands(offset)
        elif mode == COMMAND_MODES.EDIT:
            self._render_edit_commands(offset)
        else:
            self._clear_commands()

    def edit_text(self, text, offset):  # noqa: 901
        Y_ORIGIN = offset + Y_OFFSET + MARGIN + NEXT_LINE
        X_ORIGIN = X_OFFSET + MARGIN * 5 + 2

        tracker = HorizontalTracker(text, X_ORIGIN, self.cols)
        self.stdscr.addstr(Y_ORIGIN, X_ORIGIN, tracker.get_hellip_string(), self.color.blue)

        self.clear_leftovers()
        self.refresh()
        try:
            # show cursor
            curses.curs_set(True)
            while True:
                key = self.stdscr.getch()
                if key in self.commands.enter:
                    break
                elif key in self.commands.escape:
                    tracker.erase_string()
                    break
                elif key == curses.KEY_LEFT:
                    tracker.move_left()
                elif key == 262:  # fn + KEY_LEFT
                    tracker.move_to_start()
                elif key == 360:  # fn + KEY_RIGHT
                    tracker.move_to_end()
                elif key == curses.KEY_RIGHT:
                    tracker.move_right()
                elif key == 8 or key == 127 or key == curses.KEY_BACKSPACE:
                    tracker.delete()
                elif key == 330:  # fn + KEY_BACKSPACE
                    tracker.delete_backwards()
                elif not curses.keyname(key).startswith(b"KEY_"):
                    tracker.add(chr(key))

                # clear the line and rewrite string
                self.stdscr.move(Y_ORIGIN, X_ORIGIN)
                self.clear_leftovers()
                self.stdscr.addstr(Y_ORIGIN, X_ORIGIN, tracker.get_hellip_string(), self.color.blue)

                # move cursor to correct place and refresh screen
                self.stdscr.move(Y_ORIGIN, tracker.get_cursor_pos())
                self.stdscr.refresh()
        finally:
            curses.curs_set(False)
        return tracker.get_string()
