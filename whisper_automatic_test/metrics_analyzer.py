class MetricsAnalyzer:
    _scenarios = []
    _suggestions_responses = []

    def __init__(self, scenarios, suggestions_responses):
        self._scenarios = scenarios
        self._suggestions_responses = suggestions_responses

    def calculate_average_system_response_time(self):
        sum_of_system_response_time = 0
        for suggestions_response in self._suggestions_responses:
            sum_of_system_response_time += suggestions_response.get_timestamp_received_response() -\
                                            suggestions_response.get_timestamp_sent_request()
        return sum_of_system_response_time / len(self._suggestions_responses)

    def calculate_messages_number(self):
        messages_number = 0
        for scenario in self._scenarios:
            messages_number += len(scenario.get_requests())
        return messages_number

    def calculate_mean_position_of_chosen_suggestion(self):
        raise NotImplementedError()

    def calculate_total_number_of_suggestions_updates(self):
        raise NotImplementedError()

    def calculate_number_of_unwanted_suggestions_updates(self):
        raise NotImplementedError()

    def calculate_number_of_selected_suggestions(self):
        raise NotImplementedError()

    def calculate_number_of_modified_suggestions(self):
        raise NotImplementedError()

    def calculate_number_of_opened_suggestions(self):
        raise NotImplementedError()

    def calculate_number_of_suggested_questions(self):
        raise NotImplementedError()

    def calculate_number_of_suggested_links(self):
        raise NotImplementedError()

    def calculate_mean_confidence_level_of_selected_suggestions(self):
        raise NotImplementedError()

    def calculate_mean_confidence_level_of_selected_and_modified_suggestions(self):
        raise NotImplementedError()
