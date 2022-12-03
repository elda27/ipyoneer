from __future__ import annotations

from ast import AST
from datetime import datetime, timedelta
from typing import Iterator


class TimerManager:
    def __init__(self) -> None:
        self.timers: list[Timer] = []
        self.timer_stack: list[Timer] = []

    def append(self, timer: Timer) -> None:
        self.timers.append(timer)

    def render(display: bool = True):
        pass


class Timer:
    def __init__(
        self,
        manager: TimerManager,
        line: int,
        indent: int,
        statement: AST,
        parent: Timer = None,
    ) -> None:
        """Create a new timer

        Parameters
        ----------
        manager : TimerManager
            timer manager
        line : int
            line number
        indent : int
            level of code indent
        statement : AST
            statement of the target line
        parent : Timer
            parent timer
        """
        self.manager = manager
        self.line_number = line
        self.statement = statement
        self.indent = indent
        self.parent = parent
        self._start: datetime | None = None
        self.children: list[Timer] = []
        self.durations: list[timedelta] = []

    def __enter__(self) -> Timer:
        self._start = datetime.now()
        self.manager.append(self)
        self.parent.append_child(self)
        return self

    def __exit__(self, *_):
        self.durations.append(datetime.now() - self._start)

    def elapsed_times(self) -> Iterator[float]:
        """Get total elapsed time in seconds"""
        for d in self.durations:
            yield d.total_seconds()

    def duration(self) -> float:
        """Get total duration in seconds"""
        return sum(self.elapsed_times()) - sum(c.elapsed_times() for c in self.children)

    def append_child(self, child: Timer):
        """Append a child timer for calculation duration.

        Parameters
        ----------
        child : Timer
            child timer
        """
        self.children.append(child)
