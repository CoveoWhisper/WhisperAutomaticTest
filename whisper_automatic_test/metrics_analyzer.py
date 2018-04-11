class MetricsAnalyzer:
    _scenarios = []
    _suggestions_responses = []

    def __init__(self, scenarios, suggestions_responses):
        self._scenarios = scenarios
        self._suggestions_responses = suggestions_responses

    def calculate_average_system_response_time(self):
        average_system_response_time = 0
        for suggestions_response in self._suggestions_responses:
            average_system_response_time += suggestions_response.get_timestamp_received_response() - suggestions_response.get_timestamp_sent_request()
        return average_system_response_time / len(self._suggestions_responses)

    def calculate_messages_number(self):
        messages_number = 0
        for scenario in self._scenarios:
            messages_number += len(scenario.get_requests())
        return messages_number
