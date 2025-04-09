from models.action import Action
from models.verein import Verein


class Person:
    _id_counter: int = 0

    def __init__(self, zielstation: str, verein: str | Verein, zufriedenheit: int = 10,
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
    def __init__(self, people: dict[tuple[str, Verein], int] | list[Person] | None = None):
        self.people: list[Person] = []
        # used to register the actions of persons in the current simulation tick (will be reset after satisfaction values are updated)
        self.person_current_tick_action: dict[Person, Action] = {}

        if people is None:
            return

        if people is isinstance(people, list):
            for person in people:
                self.add_person(person)

        for (ziel, verein), anzahl in people.items():
            for _ in range(anzahl):
                self.add_person(Person(ziel, verein))

    def __str__(self):
        string: str = f'Person Handler: {len(self.people)} Person'

        if len(self.people) != 1:
            string += "en"

        for i in range(len(self.people)):
            string += f'\n{(i + 1)}: {self.people[i]}'

        return string

    def add_person(self, person: Person):
        self.people.append(person)

    def update_person(self, person: Person | int,
                      zufriedenheit: int | None = None, location: str | None = None):

        if isinstance(person, int):
            person_id = person
        else:
            person_id = person.id

        for person in self.people:
            if person.id != person_id:
                continue

            if zufriedenheit is not None:
                person.update_zufriedenheit(zufriedenheit)

            if location is not None:
                person.update_location(location)

            return

    def get_people_at_location(self, location: str, include_arrived_people: bool = False) -> list[Person]:

        persons_at_location = [person for person in self.people if person.current_position == location and
                               (include_arrived_people or not person.has_arrived())]

        return persons_at_location

    def average_satisfaction(self) -> float:
        sum_satisfaction = 0

        for person in self.people:
            sum_satisfaction += person.get_current_zufriedenheit()

        return sum_satisfaction / len(self.people)

    def set_person_action(self, person: Person, action: Action):
        self.person_current_tick_action[person] = action

    def set_people_actions(self, actions: list[(Person, Action)]):
        for person, action in actions:
            self.set_person_action(person, action)

    # def calculate_satisfactions_and_reset_tick_actions(self):
    #     no_action_people = [person for person in self.people if person not in self.person_current_tick_action.keys()]
    #     for person in no_action_people:
    #         if self.person_current_tick_action[person] == Action.NO_ACTION:
    #             continue
    #         if self.person_current_tick_action[person] == Action.WAITING:
    #             person.update_zufriedenheit(person.get_current_zufriedenheit() - 1)
    #         elif self.person_current_tick_action[person] == Action.DRIVING:
