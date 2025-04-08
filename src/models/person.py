from models.verein import Verein

class Person:
    _id_counter: int = 0

    def __init__(self, zielstation: str, verein: str | Verein, zufriedenheit: int = 10, current_position: str = 'Stadion'):
        self.id = Person._id_counter
        Person._id_counter += 1

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
        return f'Id: {self.id}, Location: {self.current_position}, Ziel: {self.zielstation}, Verein: {self.verein}'

    def get_current_zufriedenheit(self) -> int:
        return self.zufriedenheit[-1]

    def update_zufriedenheit(self, zufriedenheit: int):
        self.zufriedenheit.append(zufriedenheit)

    def has_arrived(self) -> bool:
        return self.current_position == self.zielstation

    def update_location(self, location: str):
        self.current_position = location

class PersonHandler:
    def __init__(self, persons: dict[tuple[str, Verein], int] | None = None):
        self.persons: list[Person] = []

        if persons is None:
            return

        for (ziel, verein), anzahl in persons.items():
            for _ in range(anzahl):
                self.add_person(Person(ziel, verein))

    def __str__(self):
        string: str = f'Person Handler: {len(self.persons)} Person'

        if len(self.persons) != 1:
            string += "en"

        for i in range(len(self.persons)):
            string += f'\n{(i+1)}: {self.persons[i]}'

        return string

    def add_person(self, person: Person):
        self.persons.append(person)

    def get_persons_at_location(self, location: str, include_arrived_people: bool = False) -> list[Person]:

        persons_at_location = [person for person in self.persons if person.current_position == location and
                               (include_arrived_people or not person.has_arrived())]

        return persons_at_location