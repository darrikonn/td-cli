import random
import tempfile
from subprocess import call

from pkg_resources import get_distribution


def generate_random_int():
    return "%06i" % random.randrange(10 ** 6)


def get_user_input(editor, initial_message=b""):
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        tf.flush()
        call([editor, "+set backupcopy=yes", tf.name])

        tf.seek(0)
        edited_message = tf.read()
        return edited_message.decode("utf-8").strip()


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
    return get_distribution("td-cli").version


def strikethrough(string):
    return "\u0336".join("{string}\u0336".format(string=string))


def hellip_prefix(string, sub_length):
    return "…" + string[sub_length:]


def hellip_postfix(string, sub_length):
    return string[:sub_length] + "…"
