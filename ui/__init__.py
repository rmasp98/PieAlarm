__all__ = ["controller"]
import enum


class Screen(enum.Enum):
    HOME = 0
    VIEW = 1
    EDIT = 2
    SNOOZE = 3
    SETTINGS = 4
    PLAYER = 5


from ui.controller import UiController as Ctrl
