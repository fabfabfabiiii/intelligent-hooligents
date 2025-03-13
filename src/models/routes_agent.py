from mesa import Agent, Model
import networkx as nx
import random
import math
from .streckennetz import Streckennetz
from typing import List, Tuple, Set
from itertools import combinations

class RoutesAgent(Agent):
    def __init__(self, model, main_station_node_id: str, start_node_id: str):
        super().__init__(model)
        self.main_station = main_station_node_id
        self.start_node = start_node_id

    def divide_graph(self, streckennetz: Streckennetz, subgraph_count: int) -> List[Streckennetz]:
        """
        Divide the network into subgraphs, each containing the main station and start node,
        and each forming a cycle.

        Args:
            streckennetz: The complete network to divide
            subgraph_count: Number of subgraphs to create

        Returns:
            List of Streckennetz subgraphs
        """
        # Ensure the main station and start node are in the graph
        if self.main_station not in streckennetz.nodes or self.start_node not in streckennetz.nodes:
            raise ValueError("Main station or start node not found in the network")

        # First try geometric division
        subgraphs = self._divide_by_geometry(streckennetz, subgraph_count)

        # If geometric division fails, try random partitioning
        if not subgraphs:
            subgraphs = self._divide_by_random_partitioning(streckennetz, subgraph_count)

        # If random partitioning fails, fallback to spanning tree approach
        if not subgraphs:
            subgraphs = self._divide_by_spanning_tree(streckennetz, subgraph_count)

        return subgraphs

    def _divide_by_random_partitioning(self, streckennetz: Streckennetz, subgraph_count: int) -> List[Streckennetz]:
        """
        Try to divide the network using random partitioning of nodes.

        Args:
            streckennetz: The complete network to divide
            subgraph_count: Number of subgraphs to create

        Returns:
            List of Streckennetz subgraphs or empty list if valid partitioning not found
        """
        # Get all nodes except the main station and start node
        regular_nodes = [node for node in streckennetz.nodes
                         if node != self.main_station and node != self.start_node]

        # Try different partitions until we find valid ones
        max_attempts = 100
        attempts = 0

        while attempts < max_attempts:
            attempts += 1

            # Create random partitions
            partitions = []
            remaining_nodes = regular_nodes.copy()
            random.shuffle(remaining_nodes)  # Shuffle nodes for better random distribution

            # Distribute nodes roughly evenly among partitions
            nodes_per_partition = len(remaining_nodes) // subgraph_count

            for i in range(subgraph_count - 1):
                if not remaining_nodes:
                    break

                # Select nodes for this partition
                if nodes_per_partition < len(remaining_nodes):
                    partition_nodes = remaining_nodes[:nodes_per_partition]
                    remaining_nodes = remaining_nodes[nodes_per_partition:]
                else:
                    partition_nodes = remaining_nodes
                    remaining_nodes = []

                # Always include main station and start node
                partition_nodes = [self.main_station, self.start_node] + partition_nodes
                partitions.append(partition_nodes)

            # Last partition gets any remaining nodes
            if remaining_nodes:
                partitions.append([self.main_station, self.start_node] + remaining_nodes)

            # Create subgraphs and check if they meet the requirements
            valid_subgraphs = []

            for node_set in partitions:
                subgraph = streckennetz.create_subgraph(node_set)

                # Check if subgraph is a network (has a Hamiltonian cycle)
                if subgraph.is_network():
                    valid_subgraphs.append(subgraph)
                else:
                    # This partition doesn't work
                    break

            # If we have the right number of valid subgraphs, return them
            if len(valid_subgraphs) == min(subgraph_count, len(partitions)):
                return valid_subgraphs

        # If we couldn't find valid partitions
        return []

    def _divide_by_spanning_tree(self, streckennetz: Streckennetz, subgraph_count: int) -> List[Streckennetz]:
        """
        Divide the network using distance-based approach.

        Args:
            streckennetz: The complete network to divide
            subgraph_count: Number of subgraphs to create

        Returns:
            List of Streckennetz subgraphs
        """
        # We'll use a graph to compute shortest paths since streckennetz doesn't have this functionality
        graph = streckennetz.convert_to_networkx()

        # Get shortest paths from main station to all other nodes
        paths = nx.shortest_path(graph, source=self.main_station)

        # Sort nodes by path length (distance from main station)
        sorted_nodes = sorted(paths.keys(), key=lambda x: len(paths[x]))

        # Remove main station and start node from sorted list
        sorted_regular_nodes = [node for node in sorted_nodes
                                if node != self.main_station and node != self.start_node]

        # Create subgraphs
        subgraphs = []

        # Distribute nodes among subgraphs
        for i in range(subgraph_count):
            start_idx = i * len(sorted_regular_nodes) // subgraph_count
            end_idx = (i + 1) * len(sorted_regular_nodes) // subgraph_count

            # Select nodes for this subgraph
            subgraph_nodes = [self.main_station, self.start_node]
            subgraph_nodes.extend(sorted_regular_nodes[start_idx:end_idx])

            # Create the subgraph
            subgraph = streckennetz.create_subgraph(subgraph_nodes)
            subgraphs.append(subgraph)

        return subgraphs

    def _divide_by_geometry(self, streckennetz: Streckennetz, subgraph_count: int) -> List[Streckennetz]:
        """
        Divide the network geometrically based on node coordinates.

        Args:
            streckennetz: The complete network to divide
            subgraph_count: Number of subgraphs to create

        Returns:
            List of Streckennetz subgraphs
        """
        # Get all nodes except main_station and start_node
        regular_nodes = [node for node in streckennetz.nodes
                         if node != self.main_station and node != self.start_node]

        # Extract coordinates
        coordinates = [streckennetz.node_coordinates[node] for node in regular_nodes]

        # Find bounding box
        if not coordinates:
            return []

        min_x = min(x for x, _ in coordinates)
        max_x = max(x for x, _ in coordinates)
        min_y = min(y for _, y in coordinates)
        max_y = max(y for _, y in coordinates)

        # Determine how to divide the space
        # Try different division approaches: horizontal slices, vertical slices, or grid
        subgraphs = []

        # Try horizontal slicing first
        horizontal_regions = []
        height = max_y - min_y
        region_height = height / subgraph_count

        for i in range(subgraph_count):
            region_min_y = min_y + i * region_height
            region_max_y = min_y + (i + 1) * region_height if i < subgraph_count - 1 else max_y + 1

            # Get nodes in this region
            region_nodes = [node for node in regular_nodes
                            if region_min_y <= streckennetz.node_coordinates[node][1] < region_max_y]

            # Always include main station and start node
            region_nodes = [self.main_station, self.start_node] + region_nodes
            subgraph = streckennetz.create_subgraph(region_nodes)

            # Only add if the subgraph meets requirements
            if subgraph.is_network():
                horizontal_regions.append(subgraph)

        # If horizontal slicing worked, return it
        if len(horizontal_regions) == subgraph_count:
            return horizontal_regions

        # Try vertical slicing
        vertical_regions = []
        width = max_x - min_x
        region_width = width / subgraph_count

        for i in range(subgraph_count):
            region_min_x = min_x + i * region_width
            region_max_x = min_x + (i + 1) * region_width if i < subgraph_count - 1 else max_x + 1

            # Get nodes in this region
            region_nodes = [node for node in regular_nodes
                            if region_min_x <= streckennetz.node_coordinates[node][0] < region_max_x]

            # Always include main station and start node
            region_nodes = [self.main_station, self.start_node] + region_nodes
            subgraph = streckennetz.create_subgraph(region_nodes)

            # Only add if the subgraph meets requirements
            if subgraph.is_network():
                vertical_regions.append(subgraph)

        # If vertical slicing worked, return it
        if len(vertical_regions) == subgraph_count:
            return vertical_regions

        # If simple slicing doesn't work, try a more balanced approach with k-means-like clustering
        # Group nodes based on their distance from each other

        # Create centers by dividing the space evenly
        centers = []
        if subgraph_count == 2:
            # For 2 subgraphs, divide diagonally
            centers = [(min_x + width / 4, min_y + height / 4),
                       (min_x + 3 * width / 4, min_y + 3 * height / 4)]
        else:
            # For more subgraphs, create a grid of centers
            grid_size = int(math.sqrt(subgraph_count))
            x_step = width / grid_size
            y_step = height / grid_size

            for i in range(grid_size):
                for j in range(grid_size):
                    if len(centers) < subgraph_count:
                        centers.append((min_x + (i + 0.5) * x_step,
                                        min_y + (j + 0.5) * y_step))

        # Assign nodes to centers
        for _ in range(5):  # Run a few iterations to improve clusters
            clusters = [[] for _ in range(subgraph_count)]

            # Assign each node to nearest center
            for node in regular_nodes:
                x, y = streckennetz.node_coordinates[node]
                distances = [math.sqrt((x - cx) ** 2 + (y - cy) ** 2) for cx, cy in centers]
                nearest_center = distances.index(min(distances))
                clusters[nearest_center].append(node)

            # Update centers
            for i, cluster in enumerate(clusters):
                if cluster:
                    avg_x = sum(streckennetz.node_coordinates[node][0] for node in cluster) / len(cluster)
                    avg_y = sum(streckennetz.node_coordinates[node][1] for node in cluster) / len(cluster)
                    centers[i] = (avg_x, avg_y)

        # Create subgraphs from clusters
        cluster_subgraphs = []
        for cluster in clusters:
            if cluster:
                subgraph_nodes = [self.main_station, self.start_node] + cluster
                subgraph = streckennetz.create_subgraph(subgraph_nodes)
                if subgraph.is_network():
                    cluster_subgraphs.append(subgraph)

        # If clustering approach worked, return it
        if len(cluster_subgraphs) == subgraph_count:
            return cluster_subgraphs

        # If all approaches fail, fallback to original methods
        return []

    # def step(self):
    #     """Mesa Agent step Funktion."""
    #     if not self.routes:
    #         self.routes = self.divide_graph()