import os
import random
import shlex
import subprocess
import tempfile
from importlib.metadata import PackageNotFoundError, version
from os import get_terminal_size as os_get_terminal_size

from todo.settings import config


def generate_random_int():
    return "%06i" % random.randrange(10**6)


def get_user_input(editor: str, initial_message=b"") -> str:
    fd, temp_path = tempfile.mkstemp(suffix=f".{config['format']}")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as tf:
            tf.write(initial_message.decode("utf-8"))
            tf.flush()

        parts = shlex.split(editor)
        editor_name = os.path.basename(parts[0]).lower()

        if "vim" in editor_name:
            parts.extend(["-c", "set backupcopy=yes"])
        elif editor_name in {"code", "code-insiders"} and "--wait" not in parts:
            parts.append("--wait")
        elif editor_name in {"subl", "sublime_text"} and "-w" not in parts:
            parts.append("-w")
        elif editor_name in {"atom"} and "--wait" not in parts:
            parts.append("--wait")

        subprocess.run([*parts, temp_path], check=True)

        with open(temp_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    finally:
        try:
            os.remove(temp_path)
        except Exception:
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
