from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
from models.optimization.transport_optimization import TransportOptimization
from models.streckennetz import Streckennetz


class passenger_exchange_optimizer(PassengerExchangeHandler):
    """
    This class is responsible for optimizing the passenger exchange process.
    It uses a greedy algorithm to find the best possible passenger exchange.
    """

    def __init__(self, streckennetz: Streckennetz):
        super().__init__()
        self.streckennetz = streckennetz

    def handle_passenger_exchange(self, route: list[str], capacity: int, passengers: list[str],
                                  persons_at_location: list[str]) -> tuple[list[str], list[str]]:
        transport_optimization = TransportOptimization(self.streckennetz)
        transport_optimization.prepare_optimization(capacity, route, passengers, persons_at_location)
        return [], []
