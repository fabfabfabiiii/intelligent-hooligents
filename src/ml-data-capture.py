import random
import time

import config
from models.action import Action
from models.impl.ImplRouteCalculator import ImplRouteCalculator
from models.intelligent_hooligents_model import IntelligentHooligentsModel
from models.passenger_exchange_optimizer import PassengerExchangeOptimizer
from models.person import Person
from models.person_handler import PersonHandler
from models.streckennetz import Streckennetz
from models.verein import Verein


class GraphParams:
    def __init__(self, num_nodes: int, edge_probability: float, width: int, height: int):
        self.num_nodes = num_nodes
        self.edge_probability = edge_probability
        self.width = width
        self.height = height


def create_model(graph_params: GraphParams, num_busses: int, num_people: int, bus_speed: int,
                 current_action_values: (int, Verein, bool, list[int], Action, int)):
    # Create Streckennetz
    streckennetz = Streckennetz.create_graph(
        graph_params.num_nodes,
        float(graph_params.edge_probability) / 100,
        graph_params.width,
        graph_params.height,
    )

    route_calculator = ImplRouteCalculator()
    passenger_exchange_handler = PassengerExchangeOptimizer(streckennetz)
    person_handler: PersonHandler = PersonHandler(dict[tuple[str, Verein], int]())

    for i in range(100):
        person_handler.add_person(Person(f'{random.randint(2, streckennetz.num_nodes)}',
                                         random.choice(list(Verein)), current_position='1'))

    stadium_node_id = "1"

    # Create model
    model = IntelligentHooligentsModel(
        graph=streckennetz,
        stadium_node_id=stadium_node_id,
        route_calculator=route_calculator,
        passenger_exchange_handler=passenger_exchange_handler,
        person_handler=person_handler,
        num_busses=num_busses,
        num_people=num_people,
        bus_speed=bus_speed,
        ml_data_tracker=current_action_values,
    )

    return model


def main():
    random.seed(config.SEED)

    action_history = []

    for j in range(30):
        # Define graph parameters
        graph_params = GraphParams(num_nodes=30, edge_probability=60, width=100, height=100)
        num_busses = 3
        num_people = 200
        bus_speed = 10
        current_action_values = []
        model = create_model(graph_params, num_busses, num_people, bus_speed, current_action_values)

        for i in range(200):
            model.step()
            if current_action_values:
                action_history += current_action_values
            current_action_values.clear()

    # id: 3, verein: "club_a", ist_angekommen: "yes"/"no", zufriedenheit: [neuerster, 2. neuster, .. 5. neuster]  , action: "DRIVING" | y: 20
    action_csv = "id,verein,ist_angekommen,zufriedenheit_1,zufriedenheit_2,zufriedenheit_3,zufriedenheit_4,zufriedenheit_5,action,y\n"

    for current_item in action_history:
        # format csv
        parts_satisfaction = ','.join(map(str, current_item[3]))
        action_csv += f"{current_item[0]},{current_item[1]},{current_item[2]},{parts_satisfaction},{current_item[4]},{current_item[5]}\n"

    # Write the CSV data to a file
    with open("ml_data.csv", "w") as file:
        file.write(action_csv)


if __name__ == "__main__":
    main()
