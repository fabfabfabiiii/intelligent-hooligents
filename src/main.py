from src.models.graph_reader import load_streckennetz
from src.models.streckennetz import Streckennetz


def main():
    print('Intelligent Agents')

    netz: Streckennetz = load_streckennetz("../resources/Verkehrsnetz.graphml")

    print(netz)

if __name__ == '__main__':
    main()