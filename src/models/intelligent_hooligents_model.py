import mesa
import networkx as nx

from models.bus_agent import BusAgent
from models.person import Person
from models.streckennetz import Streckennetz


class IntelligentHooligentsModel(mesa.Model):
    """Intelligent hooligents model."""

    def __init__(self, graph: Streckennetz | nx.Graph, stadium_node_id: int, num_busses: int = 1, num_people: int= 100):
        super().__init__()
        self.grid = mesa.space.NetworkGrid(graph if isinstance(graph, nx.Graph) else graph.convert_to_networkx())
        for i in range(num_busses):
            agent = BusAgent(self, capacity=10) # todo make capacity configurable
            self.agents.add(agent)
            self.grid.place_agent(agent, stadium_node_id)
        # self.people: list[Person] = []

    def step(self):
        """Advance the model by one step."""
        self.agents.do("step")