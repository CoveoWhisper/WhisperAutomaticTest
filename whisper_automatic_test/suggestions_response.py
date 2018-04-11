class SuggestionsResponse:
    _suggestions = None
    _timestamp_sent_request = None
    _timestamp_received_response = None

    def __init__(self, suggestions, timestamp_sent_request, timestamp_received_response):
        self._suggestions = suggestions
        self._timestamp_sent_request = timestamp_sent_request
        self._timestamp_received_response = timestamp_received_response

    def get_suggestions(self):
        return self._suggestions

    def get_timestamp_sent_request(self):
        return self._timestamp_sent_request

    def get_timestamp_received_response(self):
        return self._timestamp_received_response


