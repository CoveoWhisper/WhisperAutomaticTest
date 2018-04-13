from whisper_automatic_test.exceptions.no_requests_exception import NoRequestsException
from whisper_automatic_test.exceptions.no_suggestions_responses_exception import NoSuggestionsResponsesException
from whisper_automatic_test.exceptions.no_suggestions_responses_for_every_requests_exception import NoSuggestionsResponsesForEveryRequestsException


def get_selected_suggestion(suggestions, data_to_find_in_suggestions):
    for data in data_to_find_in_suggestions:
        for suggestion in suggestions:
            if suggestion.get_data() == data:
                return {(suggestions.index(suggestion) + 1): suggestion}
    return None


def get_selected_suggestions(suggestions_responses, requests):
    selected_suggestions = {}
    for i, suggestions_response in enumerate(suggestions_responses):
        selected_suggestion = get_selected_suggestion(
            suggestions_response.get_suggestions(),
            requests[i].get_data())
        if selected_suggestion:
            selected_suggestions.update(selected_suggestion)
    return selected_suggestions


def analyse_same(request, current_suggestions_responses, previous_suggestions_responses):
    if request.get_success_condition() != 'same':
        return False
    if set(current_suggestions_responses) == set(previous_suggestions_responses):
        return True
    return False


def analyse_link_or_question_with_request_data(request, current_suggestions_responses):
    if request.get_success_condition() == 'same' or not request.get_data():
        return False
    for data in request.get_data():
        for suggestion in current_suggestions_responses:
            if request.get_success_condition() == suggestion.get_type() and data == suggestion.get_data():
                return True
    return False


def analyse_link_or_question_without_request_data(request, current_suggestions_responses):
    if request.get_success_condition() == 'same' or request.get_data():
        return False
    for suggestion in current_suggestions_responses:
        if request.get_success_condition() == suggestion.get_type():
            return True
    return False


class SuggestionsResponsesAnalyzer:
    def __init__(self, scenarios, suggestions_responses):
        self._scenarios = scenarios
        self._requests = []
        for scenario in scenarios:
            self._requests += scenario.get_requests()
        self._suggestions_responses = suggestions_responses
        self.raise_if_there_is_no_request_in_scenarios()
        self.raise_if_there_is_no_suggestions_responses()
        self.raise_if_there_is_not_a_suggestions_response_for_every_request()

    def raise_if_there_is_no_request_in_scenarios(self):
        if not self._requests:
            raise NoRequestsException('No requests')

    def raise_if_there_is_no_suggestions_responses(self):
        if not self._suggestions_responses:
            raise NoSuggestionsResponsesException('No suggestions responses to analyze')

    def raise_if_there_is_not_a_suggestions_response_for_every_request(self):
        if len(self._requests) != len(self._suggestions_responses):
            raise NoSuggestionsResponsesForEveryRequestsException(
                'There is not a suggestions response for every request')

    def analyze(self):
        analysis = []
        previous_suggestions_responses = []
        for i, request in enumerate(self._requests):
            current_suggestions_responses = self._suggestions_responses[i].get_suggestions()
            result = analyse_same(request, current_suggestions_responses, previous_suggestions_responses)
            result = result or analyse_link_or_question_with_request_data(request, current_suggestions_responses)
            result = result or analyse_link_or_question_without_request_data(request, current_suggestions_responses)
            analysis.append('success') if result else analysis.append('fail')
            previous_suggestions_responses = current_suggestions_responses
        return analysis

    def analyze_and_print(self):
        analysis = self.analyze()
        analysis_position = 0
        for i, scenario in enumerate(self._scenarios):
            for request in scenario.get_requests():
                scenario_id = str(i + 1)
                request_analysis = scenario_id + ',' + request.get_person() + ',' + request.get_message() + ',' + request.get_success_condition() + ',' + request.get_raw_data() + ',' + analysis[
                    analysis_position]
                print(request_analysis)
                analysis_position += 1
