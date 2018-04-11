class MetricsAnalyzer:
    scenarios = []
    suggestions_responses = []
    average_system_response_time = None
    messages_number = None

    def __init__(self, scenarios, suggestions_responses):
        self.scenarios = scenarios
        self.suggestions_responses = suggestions_responses
        self.calculate_metrics()

    def calculate_metrics(self):
        self.calculate_average_system_response_time()
        self.calculate_messages_number()

    def calculate_average_system_response_time(self):
        average_system_response_time = 0
        for suggestions_response in self.suggestions_responses:
            average_system_response_time += suggestions_response.get_timestamp_received_response() - suggestions_response.get_timestamp_sent_request()
        self.average_system_response_time = average_system_response_time / len(self.suggestions_responses)

    def calculate_messages_number(self):
        messages_number = 0
        for scenario in self.scenarios:
            messages_number += len(scenario.get_requests())
        self.messages_number = messages_number

    def get_average_system_response_time(self):
        return self.average_system_response_time

    def get_messages_number(self):
        return self.messages_number
