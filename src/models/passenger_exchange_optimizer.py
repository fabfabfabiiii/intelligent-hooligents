import config
from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
from models.optimization.transport_optimization import TransportOptimization
from models.person import Person
from models.streckennetz import Streckennetz


class PassengerExchangeOptimizer(PassengerExchangeHandler):
    """
    This class is responsible for optimizing the passenger exchange process.
    It uses a greedy algorithm to find the best possible passenger exchange.
    """

    def __init__(self, streckennetz: Streckennetz):
        super().__init__()
        self.streckennetz = streckennetz

    def handle_passenger_exchange(self, route: list[str], capacity: int, passengers: list[Person],
                                  persons_at_location: list[Person]) \
            -> tuple[list[Person], list[Person]]:  # (alighting, boarding)
        transport_optimization = TransportOptimization(self.streckennetz)
        if not (passengers or persons_at_location):
            return [], []
        transport_optimization.prepare_optimization(capacity, route, passengers + persons_at_location)
        transport_optimization.solve()
        people_to_transport = transport_optimization.get_result()

        if config.DEBUGGING:
            print('people_to_transport')
            for person in people_to_transport:
                print(person)

        boarding_people = [person for person in people_to_transport if person not in passengers]
        alighting_people = [person for person in passengers if person not in people_to_transport]

        if config.DEBUGGING:
            print(f'Alighting:')
            for person in alighting_people:
                print(f'{person}')
            print(f'Boarding:')
            for person in boarding_people:
                print(f'{person}')

            #Personen für die Optimierung:
            print(f'Personen für Optimierung:')
            print('in Bus:')
            for person in passengers:
                print(f'{person}')
            print('an Station:')
            for person in persons_at_location:
                print(f'{person}')

        return alighting_people, boarding_people
