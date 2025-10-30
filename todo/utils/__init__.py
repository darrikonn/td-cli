import random
import tempfile
from importlib.metadata import PackageNotFoundError, version
from os import (
    fdopen as os_path_fdopen,
    get_terminal_size as os_get_terminal_size,
    remove as os_path_remove,
)
from os.path import basename as os_path_basename
from subprocess import call

from todo.settings import config


def generate_random_int():
    return "%06i" % random.randrange(10**6)


def get_user_input(editor, initial_message=b""):
    fd, temp_path = tempfile.mkstemp(suffix=f".{config['format']}")
    try:
        with os_path_fdopen(fd, "wb") as tf:
            tf.write(initial_message)
            tf.flush()

        editor_name = os_path_basename(editor).lower()
        if "vim" in editor_name:
            cmd = [editor, "+set", "backupcopy=yes", temp_path]
        else:
            cmd = [editor, temp_path]

        call(cmd)

        with open(temp_path, "r", encoding="utf-8") as f:
            edited_message = f.read().strip()

        return edited_message

    finally:
        try:
            os_path_remove(temp_path)
        except OSError:
            pass


def singular_or_plural(n):
    return "" if n == 1 else "s"


def to_lower(string):
    return string.strip().lower()


def interpret_state(state):
    if state is None:
        return ""
    elif state:
        return " completed"
    return " uncompleted"


def docstring(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__ % sub
        return obj

    return dec


def get_version():
    try:
        return version("td-cli")
    except PackageNotFoundError:
        return "unknown"


def strikethrough(string):
    return "\u0336".join("{string}\u0336".format(string=string))


def hellip_prefix(string, sub_length):
    return "…" + string[sub_length:]


def hellip_postfix(string, sub_length):
    return string[:sub_length] + "…"


def get_terminal_size():
    try:
        return os_get_terminal_size()
    except OSError:
        return 80, 43
