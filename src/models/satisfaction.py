from models.person import Person
from models.action import Action

def calculate_satisfaction(person: Person, action: Action) -> int:
    #zufriedenheit kann nicht negativ sein
    if person.get_current_zufriedenheit() <= 0:
        return 0

    #zufriedenheit bleibt gleich, wenn man ankommt
    if person.has_arrived():
        return person.get_current_zufriedenheit()
