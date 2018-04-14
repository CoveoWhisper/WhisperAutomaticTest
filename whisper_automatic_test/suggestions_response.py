class SuggestionsResponse:
    _suggestions = None
    _response_time_duration = None

    def __init__(self, suggestions, response_time_duration):
        self._suggestions = suggestions
        self._response_time_duration = response_time_duration

    def get_suggestions(self):
        return self._suggestions

    def get_response_time_duration(self):
        return self._response_time_duration
