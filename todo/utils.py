import random
import tempfile
from subprocess import call


def generate_random_hex():
    return '%06x' % random.randrange(16**6)


def get_user_input(editor, initial_message=b''):
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        tf.flush()
        call([editor, tf.name])

        tf.seek(0)
        edited_message = tf.read()
        return edited_message.decode("utf-8").strip()
