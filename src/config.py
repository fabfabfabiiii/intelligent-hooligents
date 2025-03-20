from src.models.verein import Verein

GRAPHML_PATH: str = "../resources/Verkehrsnetz.graphml"
USE_SEED: bool = True
SEED: int = 127456981
#Graph Visualization
NODE_COLOR: str = 'red'
NODE_COLOR_HIGHLIGHTED: str = 'green'
EDGE_COLOR: str = 'blue'
EDGE_COLOR_HIGHLIGHTED: str = 'pink'
PLT_FIGSIZE: tuple[int, int] = (10, 10)
FONT_SIZE: int = 10
NODE_SIZE: int = 500
FONT_WEIGHT: str = 'bold'

#Dict to create people
#{(ziel, verein): anzahl_personen}
peoples: dict[tuple[str, Verein], int] = {
    ('ziel 1', Verein.Club_A): 100,
    ('ziel 1', Verein.Club_B): 100,
    ('ziel 2', Verein.Club_A): 10,
    ('ziel 2', Verein.Club_B): 100,
    ('ziel 3', Verein.Club_A): 40,
}