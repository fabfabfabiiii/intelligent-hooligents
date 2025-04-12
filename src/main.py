import random
import config
from models.action import Action
from models.verein import Verein

from src.models.satisfaction import predict_satisfaction

def load_config():
    if config.USE_SEED:
        random.seed(config.SEED)


def main():
    load_config()

    print('Intelligent Agents')

    prediction = predict_satisfaction(Verein.Club_A, [1,2], False, Action.EXIT)

    print(f'Prediction: {prediction}')
    
if __name__ == '__main__':
    main()
