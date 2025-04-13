from models.verein import Verein


class Person:
    _id_counter: int = 0

    def __init__(self, zielstation: str, verein: str | Verein, zufriedenheit: int = 100,
                 current_position: str = 'Stadion'):
        self.id: int = Person._id_counter
        Person._id_counter += 1

        self.zielstation: str = zielstation
        self.current_position: str = current_position

        if isinstance(verein, Verein):
            self.verein: Verein = verein
        else:
            self.verein: Verein = getattr(Verein, verein)

        # Zufriedenheit ist Liste, kriegt pro ZE neue zufriedenheit
        self.zufriedenheit: list[int] = []
        self.zufriedenheit.append(zufriedenheit)

    def __str__(self):
        return f'Id: {self.id}, Location: {self.current_position}, Ziel: {self.zielstation}, Verein: {self.verein}, Zufriedenheit: {self.zufriedenheit}'

    def get_current_zufriedenheit(self) -> int:
        return self.zufriedenheit[-1]

    def update_zufriedenheit(self, zufriedenheit: int):
        self.zufriedenheit.append(zufriedenheit)

    def has_arrived(self) -> bool:
        return self.current_position == self.zielstation

    def update_location(self, location: str):
        self.current_position = location
