import pickle
import config
import pandas as pd
from sklearn.linear_model import LinearRegression

from models.person import Person
from models.action import Action
from models.verein import Verein

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

    # Zufriedenheit kann nicht negativ sein
    if current_satisfaction <= 0:
        return 0

    # Zufriedenheit bleibt gleich, wenn man ankommt
    if person.has_arrived():
        return person.get_current_zufriedenheit()

    if action == action.EXIT:
        return current_satisfaction - (3 * factor)

    if action == action.WAITING:
        return current_satisfaction - (2 * factor)

    if action == action.ENTRY:
        return current_satisfaction + 1

    if action == action.DRIVING:
        # sinke um den Faktor, wenn dieser mehr als drei Schritte gleich ist
        # ansonsten bleibe gleich
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

def _create_input_data(ist_angekommen: bool, verein: Verein, action: Action, satisfaction: list[int]) -> pd.DataFrame:
    verein_a: int = 0
    verein_b: int = 0
    verein_neutral: int = 0

    if verein == Verein.Club_A:
        verein_a = 1
    elif verein == Verein.Club_B:
        verein_b = 1
    else:
        verein_neutral = 1

    action_driving: int = 0
    action_entry: int = 0
    action_waiting: int = 0
    action_exit: int = 0

    if action == action.DRIVING:
        action_driving = 1
    elif action == action.ENTRY:
        action_entry = 1
    elif action == action.WAITING:
        action_waiting = 1
    elif action == action.EXIT:
        action_exit = 1

    # Reihenfolge der Werte ist wichtig, da diese input für ml model
    input_data: pd.DataFrame = pd.DataFrame({
        'ist_angekommen': [1 if ist_angekommen else 0],
        'zufriedenheit_1': [satisfaction[0]],
        'zufriedenheit_2': [satisfaction[1]],
        'zufriedenheit_3': [satisfaction[2]],
        'zufriedenheit_4': [satisfaction[3]],
        'zufriedenheit_5': [satisfaction[4]],
        'verein_Club A': [verein_a],
        'verein_Club B': [verein_b],
        'verein_Neutral': [verein_neutral],
        'action_DRIVING': [action_driving],
        'action_ENTRY': [action_entry],
        'action_EXIT': [action_exit],
        'action_WAITING': [action_waiting],
    })

    return input_data

# this function uses a ml model to predict the satisfaction of a person
def predict_satisfaction(verein: Verein, satisfaction: list[int], ist_angekommen: True, action: Action) -> int:
    ml_model: LinearRegression = _load_model()

    satisfaction_list: list[int] = [-1,-1,-1,-1,-1]

    length = len(satisfaction)
    for i in range(5):
        index: int = length - i - 1
        if index < 0 or index >= len(satisfaction):
            break

        satisfaction_list[4-i] = satisfaction[index]

    input_data: pd.DataFrame = _create_input_data(ist_angekommen, verein, action, satisfaction_list)
    df = pd.DataFrame(input_data)

    prediction = ml_model.predict(df)

    if config.DEBUGGING:
        print(f'Predicted satisfaction: {prediction}')

    return int(prediction)