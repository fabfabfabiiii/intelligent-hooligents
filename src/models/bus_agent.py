import mesa

from models.intelligent_hooligents_model import IntelligentHooligentsModel
from models.person import Person


class BusAgent(mesa.Agent):
    def __init__(self, model: "IntelligentHooligentsModel", capacity: int):
        super().__init__(model)
        self.capacity = capacity
        self.route : list[(str, str)] = []
        self.passengers : list[Person] = []

        # Movement tracking
        self.current_edge_index = 0
        self.progress_on_edge = 0
        self.target_node = None   # Set when route is assigned

    def step(self):
        if not self.route:
            return

        # Get the graph from the model
        graph = self.model.grid.G

        # Calculate the weight (distance) of the current edge
        edge_weight = graph[self.pos][self.target_node]['weight']

        # Advance progress along the edge
        self.progress_on_edge += 1

        # Check if we've completed the current edge
        if self.progress_on_edge >= edge_weight:
            # Move to the target node
            self.current_node = self.target_node
            self.model.grid.move_agent(self, self.current_node)

            # Reset progress and move to next edge in route
            self.progress_on_edge = 0
            self.current_edge_index += 1

            # Check if we've completed the entire route
            if self.current_edge_index >= len(self.route):
                self.route = []  # Clear route when complete
                self.current_edge_index = 0
                return

            # Set new target node
            self.target_node = self.route[self.current_edge_index][1]
