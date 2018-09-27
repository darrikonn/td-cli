from textwrap import dedent

from .base import Render


class RenderHelp(Render):
    def __init__(self, text):
        self.text = text

    def render(self, **kwargs):
        print(dedent(self.text).strip())
