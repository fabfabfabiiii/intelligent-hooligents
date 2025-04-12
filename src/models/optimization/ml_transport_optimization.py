from pyoptinterface import highs
import pyoptinterface as poi

from models.person import Person
from models.streckennetz import Streckennetz
from models.verein import Verein

class MLTransportOptimization:
    #ich glaube, es sollte unbedingt der gesamte Graph und kein Teilgraph übergeben werden
    def __init__(self, graph: Streckennetz):
        self.log: list[str] = []

        self.graph = graph
        self.persons: list[Person] = []

        self.is_optimized: bool = False
        self.is_prepared: bool = False
        self.model = highs.Model()

        #index: index of persons
        #(distance now, distance next_step, shortest_distance), -1 if unavailable
        self.distance_matrix: dict[Person, tuple[int, int, int]] = {}
        self.decision_variable_persons = None
        self.flag_only_one_team = None
        self.flag_no_team_a = None
        self.flag_no_team_b = None

    def prepare_optimization(self, capacity: int, stations: list[str], persons: list[Person]) -> bool:
        if self.is_optimized:
            self.log.append('Already optimized. Can\'t prepare optimization again')
            return False

        if self.is_prepared:
            self.log.append('Goal is already prepared. Can\'t prepare optimization again')
            return False

        self.log.append('Preparing optimization')

        self.persons = persons
        self.distance_matrix = self._create_distance_matrix(self.graph, stations, persons)

        self.decision_variable_persons = self.model.add_variables(persons, domain=poi.VariableDomain.Binary)
        self.log.append("Add Decision Variables")

        self.flag_only_one_team = self.model.add_variable(domain=poi.VariableDomain.Binary)
        self.flag_no_team_a = self.model.add_variable(domain=poi.VariableDomain.Binary)
        self.flag_no_team_b = self.model.add_variable(domain=poi.VariableDomain.Binary)
        self.log.append("Add Flags")


        #Anzahl mitgenommener Personen darf Kapazität nicht überschreiten
        self.model.add_linear_constraint(
            poi.quicksum(self.decision_variable_persons), poi.Leq, capacity)
        self.log.append("Add Linear Constraint")

        #Kein Team darf in Überzahl sein
        self.model.add_linear_constraint(
            poi.quicksum(self.decision_variable_persons[p] for p in persons if p.verein == Verein.Club_A) -
            poi.quicksum(self.decision_variable_persons[p] for p in persons if p.verein == Verein.Club_B) -
            (capacity * self.flag_only_one_team),
            poi.Leq, 0
        )

        self.model.add_linear_constraint(
            poi.quicksum(self.decision_variable_persons[p] for p in persons if p.verein == Verein.Club_B) -
            poi.quicksum(self.decision_variable_persons[p] for p in persons if p.verein == Verein.Club_A) -
            (capacity * self.flag_only_one_team),
            poi.Leq, 0
        )

        #Flag überprüfen
        #flag_only_one_team = no_team_a || no_team_b
        self.model.add_linear_constraint(
            self.flag_no_team_a + self.flag_no_team_b -
            self.flag_only_one_team * 1
            , poi.Geq, 0)

        self.model.add_linear_constraint(
            poi.quicksum(self.decision_variable_persons[p] for p in persons if p.verein == Verein.Club_A) -
            (1 - self.flag_no_team_a) * len(persons),
            poi.Leq, 0)

        self.model.add_linear_constraint(
            poi.quicksum(self.decision_variable_persons[p] for p in persons if p.verein == Verein.Club_B) -
            (1 - self.flag_no_team_b) * len(persons),
            poi.Leq, 0)

        #nehme keine Personen mit, die im Ziel sind (ich glaube das wird benötigt)
        self.model.add_linear_constraint(
            poi.quicksum(self.decision_variable_persons[p] for p in persons if self.distance_matrix[p][0] == 0),
            poi.Eq, 0)

        #nehme keine Personen mit, die nicht ankommen können (weil -1 uncool)
        self.model.add_linear_constraint(
            poi.quicksum(self.decision_variable_persons[p] for p in persons if self.distance_matrix[p][0] == -1),
            poi.Eq, 0)

        #mminimiere danach, wie viel die Personen von ihrem Zielort entfernt sind
        #obj = poi.quicksum(self.decision_variable_persons[p] * self.distance_matrix[p][2] for p in persons)
        #neue Optimierung: maximiere nach der Veränderung der mitgenommenen Leute - max_möglich
        obj = poi.quicksum(self.decision_variable_persons[p] *
                           (self.distance_matrix[p][0] - self.distance_matrix[p][1] - self.distance_matrix[p][2])
                           for p in persons)
        self.model.set_objective(obj, poi.ObjectiveSense.Maximize)
        self.log.append("Minimize Route length")

        self.is_prepared = True
        return True

    def solve(self) -> bool:
        if not self.is_prepared:
            self.log.append("Prepare optimization first")
            return False

        if self.is_optimized:
            self.log.append("Can't optimize again")
            return False

        self.log.append(f'Start optimization')
        self.model.optimize()

        self.log.append(f'Finish optimization')
        self.is_optimized = True
        return True

    def get_result(self) -> list[Person] | None:
        if not self.is_optimized or not self.is_prepared:
            self.log.append("No result available. Please solve the optimization first")
            return None

        persons_to_transport: list[Person] = [p for p in self.persons if self.model.get_variable_attribute(
            self.decision_variable_persons[p], poi.VariableAttribute.Value) > 0.9]

        return persons_to_transport

    @staticmethod
    def _create_distance_matrix(graph: Streckennetz, stations: list, persons: list[Person]) -> dict[Person, tuple[int, int, int]]:
        current_station: str = stations[0]
        next_station: str = stations[1]

        calculated_distances: dict[tuple[str, str], int] = {}
        distance_matrix: dict[Person, tuple[int, int, int]] = {}

        for person in persons:
            if (current_station, person.zielstation) not in calculated_distances:
                result = graph.get_distance(current_station, person.zielstation)
                calculated_distances[(current_station, person.zielstation)] = result if isinstance(result, int) else -1

            #wenn man vom start sein Ziel über diese Strecke nicht erreichen kann, kann man es nie erreichen
            if calculated_distances[(current_station, person.zielstation)] == -1:
                distance_matrix[person] = (-1, -1, -1)
                continue

            if (next_station, person.zielstation) not in calculated_distances:
                result = graph.get_distance(next_station, person.zielstation)
                calculated_distances[(next_station, person.zielstation)] = result if isinstance(result, int) else -1

            shortest_value = calculated_distances[(current_station, person.zielstation)]
            for station in stations:
                if (station, person.zielstation) not in calculated_distances:
                    result = graph.get_distance(station, person.zielstation)
                    calculated_distances[(station, person.zielstation)] = result if isinstance(result, int) else -1

                if shortest_value > calculated_distances[(station, person.zielstation)]:
                    shortest_value = calculated_distances[(station, person.zielstation)]

            distance_matrix[person] = ((calculated_distances[(current_station, person.zielstation)],
                                        calculated_distances[(next_station, person.zielstation)],
                                        shortest_value))

        return distance_matrix
