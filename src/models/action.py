from enum import Enum


class Action(Enum):
    ENTRY = 0  # Person steigt in Bus ein
    EXIT = 1  # Person steigt aus
    WAITING = 2  # Person wartet
    DRIVING = 3  # Person fährt weiter
    NO_ACTION = 4  # Person hat keine Aktion

    def __str__(self) -> str:
        if self.value == 0:
            return "Steige ein"
        if self.value == 1:
            return "Steige aus"
        if self.value == 2:
            return "warte"
        if self.value == 3:
            return "fahre"

        return "keine Aktion"
