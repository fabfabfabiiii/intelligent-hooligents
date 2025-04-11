from models.person import Person
from models.action import Action
from models.verein import Verein

factor_home_team: int = 1
factor_neutral: int = 2
factor_away_team: int = 3

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