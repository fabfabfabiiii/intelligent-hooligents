from abc import ABC, abstractmethod

from models.agents.bus_agent import BusAgent
from models.person import Person


class PassengerExchangeHandler(ABC):
    """
    Abstract base class for handling passenger exchanges.
    Determines which passengers get on and off the bus at a given node.
    """

    @abstractmethod
    def handle_passenger_exchange(self, bus: BusAgent) -> tuple[list[Person], list[Person]]:
        """
        Handle the passenger exchange at the bus's current node.

        :param bus: The bus agent at the current node.
        :return: A tuple containing two lists:
            - List of passengers to get off the bus.
            - List of passengers to get on the bus.
        """
        pass
