from mesa import Agent

from models.abstract import route_calculator
from models.abstract.route_calculator import RouteCalculator
from models.agents.bus_agent import BusAgent


# from models.intelligent_hooligents_model import IntelligentHooligentsModel TODO find workaround to have type infos without circular import


class RoutesAgent(Agent):
    """An agent that calculates routes for busses"""

    def __init__(self, model, route_calculator: RouteCalculator):
        super().__init__(model)
        self.route_calculator = route_calculator

    def _get_mandatory_nodes(self) -> list[str] | None:
        """
        Returns a list of mandatory nodes for the route calculation.
        """
        return None

    def _calculate_route(self) -> list[(str, str)]:
        return self.route_calculator.calculate_route(self.model.grid.G, self.pos, self._get_mandatory_nodes())

    def step(self):
        # find available busses waiting for a route
        bus_agents = [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if
                      isinstance(agent, BusAgent) and not agent.remaining_route]
        if not bus_agents:
            return
        # assign route to the first available bus agent
        bus_agents[0].remaining_route = self._calculate_route()
