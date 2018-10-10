class Request:
    _person = None
    _message = None
    _success_condition = None
    _data = None

    def __init__(self, person, message, success_condition, raw_data):
        self._person = person
        self._message = message
        self._success_condition = success_condition
        self.split_raw_data(raw_data)

    def split_raw_data(self, raw_data):
        if self._success_condition == 'question':
            delimiter = '?'
            self._data = [data + delimiter for data in raw_data.split(delimiter) if data]
        else:
            self._data = raw_data.split()

    def get_person(self):
        return self._person

    def get_message(self):
        return self._message

    def get_success_condition(self):
        return self._success_condition

    def get_data(self):
        return self._data

    def get_raw_data(self):
        return ' '.join(self._data)
