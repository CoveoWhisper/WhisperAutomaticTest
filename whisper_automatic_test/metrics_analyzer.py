def get_selected_suggestion(suggestions, data_to_find_in_suggestions):
    for data in data_to_find_in_suggestions:
        for suggestion in suggestions:
            if suggestion.get_data() == data:
                return {(suggestions.index(suggestion) + 1): suggestion}
    return None


class MetricsAnalyzer:
    def __init__(self, scenarios, suggestions_responses):
        self._requests = []
        self._suggestions_responses = []
        for scenario in scenarios:
            self._requests += scenario.get_requests()
        self._suggestions_responses = suggestions_responses

    def calculate_average_system_response_time(self):
        sum_of_system_response_time = 0
        for suggestions_response in self._suggestions_responses:
            sum_of_system_response_time += suggestions_response.get_timestamp_received_response() - \
                                           suggestions_response.get_timestamp_sent_request()
        return sum_of_system_response_time / len(self._suggestions_responses)

    def calculate_messages_number(self):
        return len(self._requests)

    def calculate_mean_position_of_chosen_suggestions(self):
        sum_of_positions_of_chosen_suggestions = 0
        selected_suggestions = self.get_selected_suggestions()
        for position in selected_suggestions.keys():
            sum_of_positions_of_chosen_suggestions += position
        return sum_of_positions_of_chosen_suggestions / len(selected_suggestions)

    def calculate_total_number_of_suggestions_updates(self):
        if len(self._suggestions_responses) == 0:
            return
        if len(self._suggestions_responses[0].get_suggestions()) == 0:
            total_number_of_suggestions_updates = 0
        else:
            total_number_of_suggestions_updates = 1
        for i in range(0, len(self._suggestions_responses) - 1):
            if len(set(self._suggestions_responses[i].get_suggestions()) - set(self._suggestions_responses[i + 1].get_suggestions())) > 0:
                total_number_of_suggestions_updates += 1
        return total_number_of_suggestions_updates

    def calculate_number_of_unwanted_suggestions_updates(self):
        number_of_unwanted_suggestions_updates = 0
        for i, request in enumerate(self._requests):
            if request.get_success_condition() == 'same':
                if (i == 0 and len(self._suggestions_responses[0].get_suggestions()) > 0) or (
                        i > 0 and len(set(self._suggestions_responses[i].get_suggestions()) - set(self._suggestions_responses[i - 1].get_suggestions())) > 0):
                    number_of_unwanted_suggestions_updates += 1
        return number_of_unwanted_suggestions_updates

    def calculate_number_of_selected_suggestions(self):
        return len(self.get_selected_suggestions())

    def calculate_number_of_suggested_questions(self):
        number_of_suggested_questions = 0
        for i, request in enumerate(self._requests):
            if request.get_success_condition() != 'same':
                for suggestion in self._suggestions_responses[i].get_suggestions():
                    if suggestion.get_type() == 'question':
                        number_of_suggested_questions += 1
        return number_of_suggested_questions

    def calculate_number_of_suggested_links(self):
        number_of_suggested_links = 0
        for i, request in enumerate(self._requests):
            if request.get_success_condition() != 'same':
                for suggestion in self._suggestions_responses[i].get_suggestions():
                    if suggestion.get_type() == 'link':
                        number_of_suggested_links += 1
        return number_of_suggested_links

    def calculate_mean_confidence_level_of_selected_suggestions(self):
        return 0

    def get_selected_suggestions(self):
        selected_suggestions = {}
        for i, suggestions_response in enumerate(self._suggestions_responses):
            selected_suggestion = get_selected_suggestion(suggestions_response.get_suggestions(), self._requests[i].get_data())
            if selected_suggestion is not None:
                selected_suggestions.update(selected_suggestion)
        return selected_suggestions
