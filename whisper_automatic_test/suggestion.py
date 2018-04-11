class Suggestion:
    _suggestion_type = None
    _data = None

    def __init__(self, suggestion_type, data):
        self._suggestion_type = suggestion_type
        self._data = data

    def get_type(self):
        return self._suggestion_type

    def get_data(self):
        return self._data
