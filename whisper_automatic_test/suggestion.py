class Suggestion:
    _suggestion_type = None
    _data = None

    def __init__(self, suggestion_type, data):
        self._suggestion_type = suggestion_type
        self._data = data

    def __repr__(self):
        return '({},{})'.format(self._suggestion_type, self._data)

    def __hash__(self):
        return hash((self._suggestion_type, self._data))

    def __eq__(self, other):
        return self._suggestion_type == other.get_type() and self._data == other.get_data()

    def get_type(self):
        return self._suggestion_type

    def get_data(self):
        return self._data
