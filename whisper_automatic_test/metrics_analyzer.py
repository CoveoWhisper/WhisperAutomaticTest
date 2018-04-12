def get_selected_suggestion(suggestions, data_to_find_in_suggestions):
    for data in data_to_find_in_suggestions:
        for suggestion in suggestions:
            if suggestion.get_data() == data:
                return {(suggestions.index(suggestion) + 1): suggestion}
    return None


class MetricsAnalyzer:
    _requests = []
    _suggestions_responses = []

    def __init__(self, scenarios, suggestions_responses):
        for scenario in scenarios:
            self._requests += scenario.get_requests()
        self._suggestions_responses = suggestions_responses

    def calculate_average_system_response_time(self):
        sum_of_system_response_time = 0
        for suggestions_response in self._suggestions_responses:
            sum_of_system_response_time += suggestions_response.get_timestamp_received_response() -\
                                            suggestions_response.get_timestamp_sent_request()
        return sum_of_system_response_time / len(self._suggestions_responses)

    def calculate_messages_number(self):
        return len(self._requests)

    def calculate_mean_position_of_chosen_suggestion(self):
        average_chosen_suggestion_position = 0
        selected_suggestions = self.get_selected_suggestions()
        for position in selected_suggestions.keys():
            average_chosen_suggestion_position += position
        return average_chosen_suggestion_position / len(selected_suggestions)

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

    def get_selected_suggestions(self):
        selected_suggestions = {}
        for i in range(0, len(self._suggestions_responses)):
            selected_suggestion = get_selected_suggestion(self._suggestions_responses[i].get_suggestions(), self._requests[i].get_data())
            if selected_suggestion is not None:
                selected_suggestions.update(selected_suggestion)
        return selected_suggestions
