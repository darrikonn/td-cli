from abc import ABC, abstractmethod

from .styles import Fore, Style


class Render(ABC):
    def _format(self, text, **kwargs):
        return text.format(
            red=Fore.RED,
            green=Fore.GREEN,
            blue=Fore.BLUE,
            white=Fore.WHITE,
            grey=Fore.GREY,
            bold=Style.BOLD,
            normal=Style.NORMAL,
            reset=Style.RESET_ALL,
            **kwargs,
        )

    @abstractmethod
    def render(self, *args, **kwargs):
        pass
