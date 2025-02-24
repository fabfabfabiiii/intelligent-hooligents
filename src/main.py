import random

from src import config

def load_config():
    if config.USE_SEED:
        random.seed(config.SEED)

def main():
    load_config()

    print('Intelligent Agents')
if __name__ == '__main__':
    main()