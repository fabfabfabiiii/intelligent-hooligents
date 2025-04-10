from enum import Enum


class Verein(Enum):
    Neutral = 0
    Club_A = 1
    Club_B = 2

    def __str__(self):
        if self.value == 0:
            return "Neutral"
        if self.value == 1:
            return "Club A"

        return "Club B"
