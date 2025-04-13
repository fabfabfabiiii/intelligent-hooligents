import mesa
import networkx as nx

from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
from models.abstract.route_calculator import RouteCalculator
from models.agents.bus_agent import BusAgent
from models.agents.routes_agent import RoutesAgent
from models.person_handler import PersonHandler
from models.streckennetz import Streckennetz


class IntelligentHooligentsModel(mesa.Model):
    """Intelligent hooligents model."""

    def __init__(self, graph: Streckennetz | nx.Graph, stadium_node_id: str, route_calculator: RouteCalculator,
                 passenger_exchange_handler: PassengerExchangeHandler, person_handler: PersonHandler,
                 num_busses: int = 1, bus_speed: int = 10, bus_capacity: int = 20):
        super().__init__()
        self.person_handler = person_handler
        self.grid = mesa.space.NetworkGrid(graph if isinstance(graph, nx.Graph) else graph.convert_to_networkx())
        for i in range(num_busses):
            agent = BusAgent(self, capacity=bus_capacity, passenger_exchange_handler=passenger_exchange_handler,
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
        self.person_handler.calculate_satisfactions_and_reset_tick_actions()
