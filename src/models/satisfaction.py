import pickle
import config

from models.person import Person
from models.action import Action
from models.verein import Verein

import pandas as pd

from sklearn.linear_model import LinearRegression

factor_home_team: int = 1
factor_neutral: int = 2
factor_away_team: int = 3

model: LinearRegression | None = None

def calculate_satisfaction(person: Person, action: Action) -> int | None:
    if action == action.NO_ACTION:
        return None

    current_satisfaction = person.get_current_zufriedenheit()
    factor: int = factor_neutral

    if person.verein == Verein.Club_A:
        factor = factor_home_team
    elif person.verein == Verein.Club_B:
        factor = factor_away_team

    #zufriedenheit kann nicht negativ sein
    if current_satisfaction <= 0:
        return 0

    #zufriedenheit bleibt gleich, wenn man ankommt
    if person.has_arrived():
        return person.get_current_zufriedenheit()

    if action == action.EXIT:
        return current_satisfaction - (3 * factor)

    if action == action.WAITING:
        return current_satisfaction - (2 * factor)

    if action == action.ENTRY:
        return current_satisfaction + 1

    if action == action.DRIVING:
        #sinke um den Faktor, wenn dieser mehr als drei Schritte gleich ist
        #ansonsten bleibe gleich
        for i in range(3):
            index: int = len(person.zufriedenheit) - (2+i)
            if index < 0 or index >= len(person.zufriedenheit):
                return current_satisfaction

            if person.zufriedenheit[index] != current_satisfaction:
                return current_satisfaction
        return current_satisfaction - factor

def _load_model() -> LinearRegression:
    global model

    if model is None:
        if config.DEBUGGING:
            print("Loading model...")

        with open(config.ML_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

    return model

def _create_input_data(ist_angekommen: bool) -> pd.DataFrame:
    #reihenfolge der Werte ist wichtig, da diese input für ml model
    input_data: pd.DataFrame = pd.DataFrame({
        'ist_angekommen': [1 if ist_angekommen else 0],
        'zufriedenheit_1': [100],
        'zufriedenheit_2': [100],
        'zufriedenheit_3': [100],
        'zufriedenheit_4': [100],
        'zufriedenheit_5': [100],
        'verein_Club A': [1],
        'verein_Club B': [0],
        'verein_Neutral': [0],
        #TODO implement ENTRY after updating ml model
        'action_DRIVING': [0],
        'action_EXIT': [1],
        'action_WAITING': [0],
    })

    return input_data

#this function uses a ml model to predict the satisfaction of an person
def predict_satisfaction(verein: Verein, satisfaction: list[int], ist_angekommen: True,action: Action) -> int:
    ml_model: LinearRegression = _load_model()

    input_data: pd.DataFrame = _create_input_data(ist_angekommen)
    df = pd.DataFrame(input_data)

    prediction = model.predict(df)

    return int(prediction)