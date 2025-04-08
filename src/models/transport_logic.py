from models.person import PersonHandler

class TransportLogic:
    def __init__(self, person_handler: PersonHandler):
        self.person_handler: PersonHandler = person_handler
