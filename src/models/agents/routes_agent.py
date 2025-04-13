from mesa import Agent

from models.abstract.route_calculator import RouteCalculator
from models.agents.bus_agent import BusAgent
from models.person import Person
from models.person_handler import PersonHandler


# from models.intelligent_hooligents_model import IntelligentHooligentsModel TODO find workaround to have type infos without circular import


class RoutesAgent(Agent):
    """An agent that calculates routes for busses"""

    def __init__(self, model, route_calculator: RouteCalculator, person_handler: PersonHandler):
        super().__init__(model)
        self.route_calculator = route_calculator
        self.person_handler: PersonHandler = person_handler
        self.bus_stations: dict[int, list[str]] = {}

    def _get_mandatory_nodes(self, bus_capacity: int) -> tuple[list[str], list[str]] | None:
        """
        Returns a list of mandatory nodes for the route calculation.
        """
        # TODO das ist nur ne Idee, kp ob das klappt
        dict_start = self._get_stations_start()

        amount: int = 0
        stations_pickup: list[str] = []

        while amount < bus_capacity and dict_start:
            station_max: str = max(dict_start, key=dict_start.get)
            amount += dict_start[station_max]
            stations_pickup.append(station_max)
            dict_start.pop(station_max)

        amount: int = 0

        dict_end = self._get_end_stations_for_persons_at(stations_pickup)

        #macht den Agenten schneller (Person wird sofort abgeholt, wenn sie die letze Person ist)
        #ansonsten geschah dies erst, wenn gerade optimiert wird und kein anderere Agent Ort auf Route hat
        if len(dict_end.keys()) == 1:
            return stations_pickup, list(dict_end.keys())

        stations_end: list[str] = []
        while amount < bus_capacity and dict_end:
            station_max: str = max(dict_end, key=dict_end.get)

            # füge Ort nur hinzu, wenn bisher kein Bus auf dem Weg dorthin ist
            if any(station_max in liste for liste in self.bus_stations.values()):
                dict_end.pop(station_max)
                continue

            if station_max not in stations_pickup:
                amount += dict_end[station_max]
                stations_end.append(station_max)

            dict_end.pop(station_max)

        return stations_pickup, stations_end

    def _change_direction(self, route: list[str]) -> list[str]:
        #leere Liste bleibt leer
        if not route:
            return route

        moved_start: list[str] = [route[-1]] + route[:-1]
        moved_start.reverse()

        return moved_start

    def _calculate_route(self, bus_capacity: int) -> list[str]:
        stations_pickup, stations_end = self._get_mandatory_nodes(bus_capacity)

        route = self.route_calculator.calculate_route(self.model.grid.G, self.pos, stations_pickup+stations_end)

        #stelle sicher, dass am Ende alle einkommen
        if len(stations_pickup) == 1 and len(stations_end) == 1:
            index_pickup: int = route.index(stations_pickup[0])
            index_end: int = route.index(stations_end[0])

            #drehe Route wenn Bus in falsche Richtung fahren will
            if index_end < index_pickup:
                return self._change_direction(route)

        return route

    def step(self):
        # find available busses waiting for a route
        bus_agents: list[BusAgent] = [agent for agent in self.model.grid.get_cell_list_contents([self.pos]) if
                                      isinstance(agent, BusAgent) and not agent.remaining_route]
        if not bus_agents:
            return

        # remove saved bus_routes
        for bus_agent in bus_agents:
            self.bus_stations.pop(bus_agent.unique_id, None)

        # assign route to the first available bus agent
        capacity = bus_agents[0].capacity
        bus_agents[0].remaining_route = self._calculate_route(capacity)
        self.bus_stations[bus_agents[0].unique_id] = bus_agents[0].remaining_route

    # key: station value: amount
    # dict start, dict endstation
    # mögliches Problem, wir wissen nicht ob diese Leute ggf in nem Bus sitzen
    # mit transport_logic könnten wir das wohl abgreifen...
    def _get_stations_start(self) -> dict[str, int]:
        dict_start: dict[str, int] = {}

        for person in self.person_handler.people:
            if person.has_arrived():
                continue

            start: str = person.current_position

            if start not in dict_start:
                dict_start[start] = 1
            else:
                dict_start[start] += 1

        return dict_start

    def _get_end_stations_for_persons_at(self, stations: list[str]) -> dict[str, int]:
        dict_end: dict[str, int] = {}

        for station in stations:
            persons: list[Person] = self.person_handler.get_people_at_location(station, False)

            for person in persons:
                end_station: str = person.zielstation

                if end_station not in dict_end:
                    dict_end[end_station] = 1
                else:
                    dict_end[end_station] += 1

        return dict_end
