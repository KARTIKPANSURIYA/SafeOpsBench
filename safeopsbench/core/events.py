"""Deterministic environment event controller."""

from collections import Counter

from safeopsbench.core.task import EventSpec


class EventController:
    """Match each task event once against execution phase and step."""

    def __init__(self, events: list[EventSpec]) -> None:
        self.events = events
        self.fired: set[int] = set()
        self.failures: Counter[str] = Counter()

    def matching(self, when: str, tool: str, step: int) -> list[tuple[int, EventSpec]]:
        matches: list[tuple[int, EventSpec]] = []
        for index, event in enumerate(self.events):
            if index in self.fired:
                continue
            trigger = event.trigger
            matched = (
                (when == "before" and trigger.before_tool == tool)
                or (when == "after" and trigger.after_tool == tool)
                or trigger.on_tool_name == tool
                or (trigger.after_n_steps is not None and step >= trigger.after_n_steps)
            )
            if matched:
                self.fired.add(index)
                matches.append((index, event))
        return matches
