from src.models.verein import Verein

class Person:
    def __init__(self, zielstation: str, verein: str | Verein, zufriedenheit: int, current_position: str = 'Stadion'):
        self.zielstation: str = zielstation
        self.current_position: str = current_position

        if isinstance(verein, Verein):
            self.verein: Verein = verein
        else:
            self.verein: Verein = getattr(Verein, verein)

        #Zufriedenheit ist Liste, kriegt pro ZE neue zufriedenheit
        self.zufriedenheit: list[int] = []
        self.zufriedenheit.append(zufriedenheit)

    def __str__(self):
        return f'Ziel: {self.zielstation}, Verein: {self.verein}'

    def get_current_zufriedenheit(self) -> int:
        return self.zufriedenheit[-1]

    def update_zufriedenheit(self, zufriedenheit: int):
        self.zufriedenheit.append(zufriedenheit)

    def has_arrived(self) -> bool:
        return self.current_position == self.zielstation

class PersonHandler:
    def __init__(self):
        self.persons: list[Person] = []

    def __str__(self):
        string: str = f'Person Handler: {len(self.persons)} Person'

        if len(self.persons) != 1:
            string += "en"

        for i in range(len(self.persons)):
            string += f'\n{(i+1)}: {self.persons[i]}'

        return string

    def add_person(self, person: Person):
        self.persons.append(person)

    def get_persons_at_location(self, location: str) -> list[Person]:
        persons_at_station: list[Person] = []

        for person in self.persons:
            if person.current_position == location:
                persons_at_station.append(person)

        return persons_at_station