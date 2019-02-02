import textwrap
from os import get_terminal_size

from .base import Render


class RenderOutputWithTextwrap(Render):
    def __init__(self, prefix, text_to_wrap):
        self.prefix = prefix
        self.text_to_wrap = text_to_wrap

    def render(self, **kwargs):
        kwargs.setdefault("subsequent_indent", " " * 10)

        cols, _ = get_terminal_size()

        wrapper = textwrap.TextWrapper(
            initial_indent=self._format(self.prefix, **kwargs),
            width=cols,
            subsequent_indent=kwargs.get("subsequent_indent"),
        )
        print(wrapper.fill(self._format(self.text_to_wrap, **kwargs)))
