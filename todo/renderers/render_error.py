from .base import Render


class RenderError(Render):
    def __init__(self, error, detailed_error, verbose, title):
        self.error = error
        self.detailed_error = detailed_error
        self.verbose = verbose
        self.title = title

    def render(self, **kwargs):
        if self.verbose:
            print(self._format("{red}{title}{reset}:", title=self.title))
            print(self._format(str(self.detailed_error), **kwargs))
        else:
            print(self._format("{red}{title}{reset}:", title=self.title))
            print(self._format(str(self.error), **kwargs))
            if self.detailed_error != self.error and not self.verbose:
                print(
                    self._format(
                        "\nRun with `{bold}--verbose/-v{reset}` to get more detailed error message",
                        **kwargs
                    )
                )
