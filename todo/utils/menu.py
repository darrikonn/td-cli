import curses
from collections import namedtuple

from todo.utils import strikethrough
from todo.constants import INTERACTIVE_COMMANDS as COMMANDS
from todo.exceptions import TodoException

X_OFFSET = 2
Y_OFFSET = 4
MARGIN = 2
NEXT_LINE = 1

NUMBER_OF_COMMANDS = 5


class Menu:
    __slots__ = ("stdscr", "color")

    commands = namedtuple(
        "Command",
        (
            COMMANDS.ADD,
            COMMANDS.DELETE,
            COMMANDS.DOWN,
            COMMANDS.EDIT,
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
        todo_name_text = "{name}".format(name=todo[1])
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN + NEXT_LINE,
            X_OFFSET + MARGIN * 5,
            ": {name}".format(name=strikethrough(todo_name_text) if is_deleted else todo_name_text),
            extra_style,
        )

    def clear_commands(self, offset):
        # clear screen for other commands
        for i in range(NUMBER_OF_COMMANDS):
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * (i + 2),
                X_OFFSET + MARGIN,
                " ",
                curses.A_BOLD | self.color.grey,
            )
            self.clear_leftovers()

    def render_commands_for_edit_mode(self, offset):
        # save
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE,
            X_OFFSET + MARGIN,
            "enter",
            curses.A_BOLD | self.color.grey,
        )
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
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * 2,
            X_OFFSET + MARGIN * 5,
            "to exit edit mode without saving",
            self.color.grey,
        )

    def render_commands(self, offset, is_deleted):
        line_count = 1
        if is_deleted:
            # recover
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN,
                "r",
                curses.A_BOLD | self.color.grey,
            )
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN * 5,
                "to recover deleted todo",
                self.color.grey,
            )
            line_count += 1

            # clear screen for other commands
            self.clear_commands(offset)
        else:
            # add
            self.stdscr.addstr(
                offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
                X_OFFSET + MARGIN,
                "a",
                curses.A_BOLD | self.color.grey,
            )
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
        self.stdscr.addstr(
            offset + Y_OFFSET + MARGIN * 2 + NEXT_LINE * line_count,
            X_OFFSET + MARGIN * 5,
            "to quit",
            self.color.grey,
        )
