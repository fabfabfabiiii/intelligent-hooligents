from mesa import Agent
from models.bus_agent import BusAgent
from models.intelligent_hooligents_model import IntelligentHooligentsModel


class RoutesAgent(Agent):
    """An agent that calculates routes for busses"""
    def __init__(self, model: IntelligentHooligentsModel):
        super().__init__(model)

    def _calculate_route(self) -> list[(str, str)]:
        # TODO implement route calculation
        return []


    def step(self):
        # find available busses waiting for a route
        bus_agents = [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if isinstance(agent, BusAgent) and not agent.route]
        if not bus_agents:
            return
        # assign route to the first available bus agent
        bus_agents.pop(0).route = self._calculate_route()