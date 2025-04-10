from models.action import Action
from models.person import Person
from models.satisfaction import calculate_satisfaction
from models.verein import Verein


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

    def calculate_satisfactions_and_reset_tick_actions(self):
        no_action_people = [person for person in self.people if person not in self.person_current_tick_action.keys()]
        self.set_people_actions([(person, Action.EXIT) for person in no_action_people])
        for person, action in self.person_current_tick_action.items():
            person.update_zufriedenheit(calculate_satisfaction(person, action))
        self.person_current_tick_action = {}
