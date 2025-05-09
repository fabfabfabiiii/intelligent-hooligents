from models.person import Person
from models.person_handler import PersonHandler
from models.action import Action

# Unused Class -> Created for initial tests
class TransportLogic:
    def __init__(self, person_handler: PersonHandler):
        self.person_handler: PersonHandler = person_handler

        # key: bus_id, value: persons in bus
        self.persons_in_bus: dict[int, list[int]] = {}

        self.moved_busses: list[int] = []
        # key: person_id, value: action
        self.actions: dict[int, Action] = {}

    # rufe nach jedem Tick auf (wenn alle agenten fertig)
    def update(self):
        for person in self.person_handler.people:
            if person.id not in self.actions and not person.has_arrived():
                self.actions[person.id] = Action.WAITING

        for person_id, action in self.actions.items():
            # TODO calculate satisfaction
            satisfaction: int = 10  # placeholder
            self.person_handler.update_person(person_id, zufriedenheit=satisfaction)

        # reset
        self.moved_busses = []
        self.actions = {}

    # gibt notwendige Informationen für einen BusAgent
    def get_people_to_transport(self, station: str) -> list[Person]:
        persons_at_station: list[Person] = self.person_handler.get_people_at_location(station, False)

        # filtere alles aus, was in diesem Tick angefahren wurde (da diese Personen noch nicht mitgenommen werden können)
        for bus_id in self.moved_busses:
            persons_at_station = [p for p in persons_at_station if p.id not in self.persons_in_bus[bus_id]]

        return persons_at_station

    # gibt, welche Personen mit BusAgent transportiert wurden
    def transported_people(self, bus_id: int, persons: list[Person], station: str) -> None:
        if bus_id not in self.persons_in_bus:
            self.persons_in_bus[bus_id] = []

        if bus_id not in self.moved_busses:
            self.moved_busses.append(bus_id)

        for person_id in self.persons_in_bus[bus_id][:]:
            if person_id in [p.id for p in persons]:
                # person bleibt im Bus → fährt weiter
                self.actions[person_id] = Action.DRIVING
            else:
                # person fährt nicht mehr mit → Ausstieg
                # eventuell noch Umstieg möglich?
                self.actions[person_id] = Action.EXIT
                self.persons_in_bus[bus_id].remove(person_id)

        for person in persons:
            if person.id not in self.persons_in_bus[bus_id]:
                # add person to bus -> Einstieg oder Umstieg
                self.persons_in_bus[bus_id].append(person.id)

                # person stieg zuvor aus
                if person.id in self.actions and self.actions[person.id] == Action.EXIT:
                    self.actions[person.id] = Action.SWITCHING
                    continue

                for b_id, p_id in {k: v for k, v in self.persons_in_bus.items()
                                   if k != bus_id}.items():

                    if person.id in p_id[:]:
                        # person steigt um
                        self.actions[person.id] = Action.SWITCHING
                        self.persons_in_bus[b_id].remove(person.id)

                self.actions[person.id] = Action.ENTRY

            self.person_handler.update_person(person, location=station)
