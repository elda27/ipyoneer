from ipyoneer.magic import PyoneerMagics
from ipyoneer.timer import Timer, TimerManager


def load_ipython_extension(ipython):
    ipython.register_magics(PyoneerMagics)


__all__ = ["Timer", "TimerManager"]
