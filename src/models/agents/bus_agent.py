import mesa

from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
# from models.intelligent_hooligents_model import IntelligentHooligentsModel TODO find workaround to have type infos without circular import
from models.person import Person, PersonHandler


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

    def _handle_node_actions(self):
        alighting_passengers, boarding_passengers = self.passenger_exchange_handler.handle_passenger_exchange(
            self.remaining_route, self.capacity, self.passengers, self.person_handler.get_persons_at_location(self.pos))
        if alighting_passengers:
            for passenger in alighting_passengers:
                self.passengers.remove(passenger)
        if boarding_passengers:
            for passenger in boarding_passengers:
                if len(self.passengers) < self.capacity:
                    self.passengers.append(passenger)
                else:
                    # Handle the case where the bus is full
                    raise Exception("Bus is full, cannot board more passengers.")
