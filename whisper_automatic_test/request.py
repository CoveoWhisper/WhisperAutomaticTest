class Request:
    _person = None
    _message = None
    _success_condition = None
    _data = None

    def __init__(self, person, message, success_condition, raw_data):
        self._person = person
        self._message = message
        self._success_condition = success_condition
        self._data = raw_data.split()

    def get_person(self):
        return self._person

    def get_message(self):
        return self._message

    def get_success_condition(self):
        return self._success_condition

    def get_data(self):
        return self._data
