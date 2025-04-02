from abc import ABC, abstractmethod
from models.person import Person


class PassengerExchangeHandler(ABC):
    """
    Abstract base class for handling passenger exchanges.
    Determines which passengers get on and off the bus at a given node.
    """

    @abstractmethod
    def handle_passenger_exchange(self, remaining_stops: list[str], bus_capacity: int, current_passengers: list[Person],
                                  people_at_station: list[Person]) -> tuple[list[Person], list[Person]]:
        """
        Handle the passenger exchange at the bus's current node.

        :param remaining_stops: List of remaining stops for the bus.
        :param bus_capacity: The capacity of the bus.
        :param current_passengers: List of current passengers on the bus.
        :param people_at_station: List of people waiting at the station.
        :return: A tuple containing two lists:
            - List of passengers to get off the bus.
            - List of passengers to get on the bus.
        """
        pass
