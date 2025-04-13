import config
from models.abstract.passenger_exchange_handler import PassengerExchangeHandler
from models.action import Action
from models.optimization.transport_optimization import TransportOptimization
from models.optimization.ml_transport_optimization import MLTransportOptimization
from models.person import Person
from models.streckennetz import Streckennetz
from models.satisfaction import predict_satisfaction


class MLPassengerExchangeHandler(PassengerExchangeHandler):
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

        if not (passengers or persons_at_location):
            return [], []

        transport_optimization = TransportOptimization(self.streckennetz)

        transport_optimization.prepare_optimization(capacity, route, passengers + persons_at_location)
        transport_optimization.solve()

        optimization_maximum: int = transport_optimization.get_optimization_value()


        predicted_satisfaction: dict[int, tuple[int, int]] = {}
        current_station: str = route[0]
        next_station: str = route[1]
        # Passenger: mitnahme → DRIVING, keine Mitnahme → EXIT
        for person in passengers:
            driving: int = predict_satisfaction(person.verein, person.zufriedenheit,
                                                    person.zielstation == next_station,
                                                    Action.DRIVING)

            satisfaction_exit: int = predict_satisfaction(person.verein, person.zufriedenheit,
                                                person.zielstation == current_station,
                                                Action.EXIT)

            predicted_satisfaction[person.id] = (driving, satisfaction_exit)

        # Wartende: mitnahme → ENTRY, keine Mitnahme → WAITING
        for person in persons_at_location:
            entry: int = predict_satisfaction(person.verein, person.zufriedenheit,
                                                person.zielstation == next_station,
                                                Action.ENTRY)

            # langer name, weil exit reserviertes wort
            waiting: int = predict_satisfaction(person.verein, person.zufriedenheit,
                                                person.zielstation == current_station,
                                                Action.WAITING)

            predicted_satisfaction[person.id] = (entry, waiting)


        ml_optimization = MLTransportOptimization(self.streckennetz)
        ml_optimization.prepare_optimization(capacity, route, passengers + persons_at_location,
                                                       predicted_satisfaction, optimization_maximum)

        ml_optimization.solve()
        people_to_transport = ml_optimization.get_result()

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