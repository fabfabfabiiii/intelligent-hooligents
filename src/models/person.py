from src.models.verein import Verein
from typing import Union

class Person:
    def __init__(self, zielstation: str, verein: Union[str, Verein], zufriedenheit: int):
        self.zielstation: str = zielstation

        if isinstance(verein, Verein):
            self.verein: Verein = verein
        else:
            self.verein: Verein = getattr(Verein, verein)

        #Zufriedenheit ist Liste, kriegt pro ZE neue zufriedenheit
        self.zufriedenheit: list = []
        self.zufriedenheit.append(zufriedenheit)

    def __str__(self):
        return f'Ziel: {self.zielstation}, Verein: {self.verein}'

    def get_current_zufriedenheit(self):
        return self.zufriedenheit[-1]

    def update_zufriedenheit(self, zufriedenheit: int):
        self.zufriedenheit.append(zufriedenheit)