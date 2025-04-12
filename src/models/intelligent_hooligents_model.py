import mesa
import networkx as nx

from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
from models.abstract.route_calculator import RouteCalculator
from models.action import Action
from models.agents.bus_agent import BusAgent
from models.agents.routes_agent import RoutesAgent
from models.person_handler import PersonHandler
from models.streckennetz import Streckennetz
from models.verein import Verein
from typing import List, Tuple


class IntelligentHooligentsModel(mesa.Model):
    """Intelligent hooligents model."""

    # id: 3, verein: "club_a", ist_angekommen: "yes"/"no", zufriedenheit: [neuerster, 2. neuster, .. 5. neuster]  , action: "DRIVING" | y: 20
    def __init__(self, graph: Streckennetz | nx.Graph, stadium_node_id: str, route_calculator: RouteCalculator,
                 passenger_exchange_handler: PassengerExchangeHandler, person_handler: PersonHandler,
                 num_busses: int = 1, num_people: int = 100, bus_speed: int = 10,
                 ml_data_tracker: List[Tuple[int, Verein, bool, List[int], Action, int | None]] = None):
        super().__init__()
        self.person_handler = person_handler
        self.ml_data_tracker = ml_data_tracker
        self.grid = mesa.space.NetworkGrid(graph if isinstance(graph, nx.Graph) else graph.convert_to_networkx())
        for i in range(num_busses):
            agent = BusAgent(self, capacity=20, passenger_exchange_handler=passenger_exchange_handler,
                             person_handler=person_handler, speed=bus_speed)  # todo make capacity configurable
            self.agents.add(agent)
            # noinspection PyTypeChecker
            self.grid.place_agent(agent, stadium_node_id)  # TODO refactor Streckennetz to use integers as ids?
        routes_agent = RoutesAgent(self, route_calculator, person_handler)
        self.agents.add(routes_agent)
        # noinspection PyTypeChecker
        self.grid.place_agent(routes_agent, stadium_node_id)  # TODO refactor Streckennetz to use integers as ids?
        # self.people: list[Person] = []

    def step(self):
        """Advance the model by one step."""
        self.agents.do("step")
        start_index = len(self.ml_data_tracker)
        current_tick_people = [person for person in self.person_handler.person_current_tick_action.keys()]
        for person in current_tick_people:
            self.ml_data_tracker.append(
                (person.id, person.verein, person.has_arrived(), self.get_padded_satisfaction(person.zufriedenheit, 5),
                 self.person_handler.person_current_tick_action[person], None))
        self.person_handler.calculate_satisfactions_and_reset_tick_actions()
        for i, person in enumerate(current_tick_people):
            self.ml_data_tracker[i + start_index] = (self.ml_data_tracker[i + start_index][0],
                                                     self.ml_data_tracker[i + start_index][1],
                                                     self.ml_data_tracker[i + start_index][2],
                                                     self.ml_data_tracker[i + start_index][3],
                                                     self.ml_data_tracker[i + start_index][4],
                                                     person.get_current_zufriedenheit())

    def get_padded_satisfaction(self, satisfaction_list, count=5):
        # Take up to the last 'count' elements, pad with -1 if needed
        padded = [-1] * count
        # Get available values (up to 'count')
        available = satisfaction_list[-count:] if satisfaction_list else []
        # Place available values at the end of the padded list
        padded[count - len(available):] = available
        return padded
