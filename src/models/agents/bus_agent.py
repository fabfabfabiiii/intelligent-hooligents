import mesa

from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
from models.action import Action
# from models.intelligent_hooligents_model import IntelligentHooligentsModel TODO find workaround to have type infos without circular import
from models.person import Person
from models.person_handler import PersonHandler
from models.verein import Verein


class BusAgent(mesa.Agent):
    def __init__(self, model, capacity: int,
                 passenger_exchange_handler: PassengerExchangeHandler, person_handler: PersonHandler, speed: int = 10):
        super().__init__(model)
        self.capacity = capacity
        self.remaining_route: list[str] = []
        self.passengers: list[Person] = []
        self.passenger_exchange_handler = passenger_exchange_handler
        self.person_handler = person_handler
        self.speed = speed

        # Movement tracking
        self.current_edge_length: int | None = None
        self.current_edge_progress: int = 0

    def step(self):
        if not self.remaining_route:
            return

        # TODO remove - only for debugging reasons
        clubA = [person for person in self.passengers if person.verein == Verein.Club_A]
        clubB = [person for person in self.passengers if person.verein == Verein.Club_B]
        neutral = [person for person in self.passengers if person.verein == Verein.Neutral]
        if ((len(clubA) > len(clubB)) and len(clubB) > 0) or ((len(clubB) > len(clubA)) and len(clubA) > 0):
            raise Exception("es gibt auf die Fresse")

        if self.current_edge_length is None:
            # We are currently at a node

            # Perform node-specific actions (e.g., passenger pickup/dropoff)
            self._handle_node_actions()

            # If there are no more destinations after handling node actions, return
            if not self.remaining_route:
                return

            # Get the next edge length to start moving
            self.current_edge_length = self.model.grid.G.edges[(self.pos, self.remaining_route[0])]['weight']
            return  # End the step after handling node actions

        # Move along the edge
        self.current_edge_progress += self.speed

        # Check if we have reached the end of the edge
        if self.current_edge_progress >= self.current_edge_length:
            # Move to the next node
            self.current_edge_length = None
            self.current_edge_progress = 0
            self.model.grid.move_agent(self, self.remaining_route.pop(0))
            for passenger in self.passengers:
                passenger.update_location(self.pos)

    def _handle_node_actions(self):
        other_busses = [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if
                        isinstance(agent, BusAgent) and agent.unique_id != self.unique_id]
        passengers_of_other_busses = [passenger for bus in other_busses for passenger in bus.passengers]
        exchangeable_people_at_station = [person for person in self.person_handler.get_people_at_location(self.pos) if
                                          person not in passengers_of_other_busses]
        alighting_passengers, boarding_passengers = self.passenger_exchange_handler.handle_passenger_exchange(
            [self.pos] + self.remaining_route, self.capacity, self.passengers, exchangeable_people_at_station)

        if alighting_passengers:
            for passenger in alighting_passengers:
                self.passengers.remove(passenger)
                print(f"Passenger {passenger.id} from bus {self.unique_id} alighted at {self.pos}.")
        if boarding_passengers:
            for passenger in boarding_passengers:
                if len(self.passengers) < self.capacity:
                    self.passengers.append(passenger)
                    print(f"Passenger {passenger.id} boarded bus {self.unique_id} at {self.pos}.")
                else:
                    # Handle the case where the bus is full
                    raise Exception("Bus is full, cannot board more passengers.")

        self._update_people_satisfactions(alighting_passengers, boarding_passengers, exchangeable_people_at_station)

    def _update_people_satisfactions(self, alighting_passengers: list[Person], boarding_passengers: list[Person],
                                     exchangeable_people_at_station: list[Person]):
        people_staying_in_bus = [passenger for passenger in self.passengers if passenger not in alighting_passengers]
        people_staying_at_station = [person for person in exchangeable_people_at_station if
                                     person not in boarding_passengers]

        self.person_handler.set_people_actions([(p, Action.EXIT) for p in alighting_passengers])
        self.person_handler.set_people_actions([(p, Action.ENTRY) for p in boarding_passengers])
        self.person_handler.set_people_actions([(p, Action.DRIVING) for p in people_staying_in_bus])
        self.person_handler.set_people_actions([(p, Action.WAITING) for p in people_staying_at_station])
