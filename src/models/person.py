from src.models.verein import Verein


class Person:
    def __init__(self, zielstation: str, verein: str, zufriedenheit: int):
        self.zielstation: str = zielstation
        self.verein: Verein = getattr(Verein, verein)

        #Zufriedenheit ist Liste, kriegt pro ZE neue zufriedenheit
        self.zufriedenheit: list = []
        self.zufriedenheit.append(zufriedenheit)

    def __str__(self):
        return f'Ziel: {self.zielstation}, Verein: {self.verein}'
