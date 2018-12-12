import math
from datetime import timedelta

from whisper_automatic_test.suggestions_responses_analyzer import get_selected_suggestions, get_requests, \
    get_selected_links
from whisper_automatic_test.utility import raise_if_there_is_no_request_in_scenarios, \
    raise_if_there_is_no_suggestions_responses, raise_if_there_is_not_a_suggestions_response_for_every_request, \
    raise_if_there_is_an_invalid_timestamp


class MetricsAnalyzer:
    def __init__(self, scenarios, suggestions_responses_for_each_scenario):
        self._requests = get_requests(scenarios)
        self._suggestions_responses = []
        for suggestions_responses_for_a_scenario in suggestions_responses_for_each_scenario:
            self._suggestions_responses += suggestions_responses_for_a_scenario
        raise_if_there_is_no_request_in_scenarios(scenarios)
        raise_if_there_is_no_suggestions_responses(suggestions_responses_for_each_scenario)
        raise_if_there_is_not_a_suggestions_response_for_every_request(
            scenarios,
            suggestions_responses_for_each_scenario
        )
        raise_if_there_is_an_invalid_timestamp(suggestions_responses_for_each_scenario)

    def calculate_average_system_response_time(self):
        sum_of_system_response_time = timedelta(seconds=0)
        for suggestions_response in self._suggestions_responses:
            sum_of_system_response_time += suggestions_response.get_response_time_duration()
        return sum_of_system_response_time / len(self._suggestions_responses)

    def calculate_messages_number(self):
        return len(self._requests)

    def calculate_mean_position_of_selected_suggestions(self):
        selected_suggestions = get_selected_suggestions(self._suggestions_responses, self._requests)
        if not selected_suggestions:
            return math.inf
        sum_of_positions = sum([selected_suggestion[0] for selected_suggestion in selected_suggestions])
        return sum_of_positions / len(selected_suggestions)

    def calculate_total_number_of_suggestions_updates(self):
        previous_suggestions = []
        number_of_suggestions_updates = 0

        for suggestions_response in self._suggestions_responses:
            current_suggestions = suggestions_response.get_suggestions()
            if set(current_suggestions) != set(previous_suggestions):
                number_of_suggestions_updates += 1
            previous_suggestions = current_suggestions

        return number_of_suggestions_updates

    def calculate_number_of_link_request(self):
        return len([_ for _, request in enumerate(self._requests) if request.get_success_condition() == 'link'])


    def calculate_number_of_unwanted_suggestions_updates(self):
        previous_suggestions = []
        number_of_unwanted_suggestions_updates = 0

        for i, request in enumerate(self._requests):
            current_suggestions = self._suggestions_responses[i].get_suggestions()
            if request.get_success_condition() == 'same':
                if set(current_suggestions) != set(previous_suggestions):
                    number_of_unwanted_suggestions_updates += 1
                    previous_suggestions = current_suggestions

        return number_of_unwanted_suggestions_updates

    def calculate_number_of_selected_link_suggestions(self):
        return len(get_selected_links(self._suggestions_responses, self._requests))

    def calculate_number_of_selected_suggestions(self):
        return len(get_selected_suggestions(self._suggestions_responses, self._requests))

    def calculate_number_of_suggested_questions(self):
        return self.get_number_of_suggestions_of_type('question')

    def calculate_number_of_suggested_links(self):
        return self.get_number_of_suggestions_of_type('link')

    def get_number_of_suggestions_of_type(self, suggestion_type):
        previous_suggestions = []
        number_of_suggestions = 0
        for suggestions_response in self._suggestions_responses:
            current_suggestions = suggestions_response.get_suggestions()
            if set(current_suggestions) != set(previous_suggestions):
                for suggestion in current_suggestions:
                    if suggestion.get_type() == suggestion_type:
                        number_of_suggestions += 1
            previous_suggestions = current_suggestions
        return number_of_suggestions

    @staticmethod
    def calculate_mean_confidence_level_of_selected_suggestions():
        return 0
