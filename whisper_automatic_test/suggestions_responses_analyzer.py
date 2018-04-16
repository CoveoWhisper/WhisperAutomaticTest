from whisper_automatic_test.exceptions.no_requests_exception import NoRequestsException
from whisper_automatic_test.exceptions.no_suggestions_responses_exception import NoSuggestionsResponsesException
from whisper_automatic_test.exceptions.no_suggestions_responses_for_every_requests_exception \
    import NoSuggestionsResponsesForEveryRequestsException


def get_selected_suggestion(suggestions, data_to_find_in_suggestions):
    for data in data_to_find_in_suggestions:
        for suggestion in suggestions:
            if suggestion.get_data() == data:
                return [(suggestions.index(suggestion) + 1), suggestion]
    return None


def get_selected_suggestions(suggestions_responses, requests):
    selected_suggestions = []
    for i, suggestions_response in enumerate(suggestions_responses):
        selected_suggestion = get_selected_suggestion(
            suggestions_response.get_suggestions(),
            requests[i].get_data())
        if selected_suggestion:
            selected_suggestions.append(selected_suggestion)
    return selected_suggestions


def analyse_same(request, current_suggestions, previous_suggestions):
    if request.get_success_condition() != 'same':
        return False
    if set(current_suggestions) == set(previous_suggestions):
        return True
    return False


def analyse_link_or_question_with_request_data(request, suggestions):
    if request.get_success_condition() == 'same' or not request.get_data():
        return ''
    for i, data in enumerate(request.get_data()):
        for j, suggestion in enumerate(suggestions):
            if request.get_success_condition() == suggestion.get_type() and data == suggestion.get_data():
                return str(i + 1) + '-' + str(j + 1)
    return ''


def analyse_link_or_question_without_request_data(request, suggestions):
    if request.get_success_condition() == 'same' or request.get_data():
        return False
    for suggestion in suggestions:
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
        previous_suggestions = []
        for i, request in enumerate(self._requests):
            current_suggestions = self._suggestions_responses[i].get_suggestions()
            is_success = analyse_same(request, current_suggestions, previous_suggestions)
            is_success |= analyse_link_or_question_without_request_data(request, current_suggestions)
            if is_success:
                analysis.append('success')
            else:
                selected_suggestion_position = analyse_link_or_question_with_request_data(request, current_suggestions)
                analysis.append('success(' + selected_suggestion_position + ')') if selected_suggestion_position \
                    else analysis.append('fail')
            previous_suggestions = current_suggestions
        return analysis

    def analyze_to_string(self):
        analysis = self.analyze()
        number_of_successful_analysis = 0
        for single_analysis in analysis:
            if 'success' in single_analysis:
                number_of_successful_analysis += 1
        analysis_position = 0
        analysis_string = 'Scenario,Person,Message,Success condition,Result,System response time\n'
        for i, scenario in enumerate(self._scenarios):
            for request in scenario.get_requests():
                scenario_id = str(i + 1)
                elements = [
                    scenario_id,
                    request.get_person(),
                    request.get_message(),
                    request.get_success_condition(),
                    analysis[analysis_position],
                    str(self._suggestions_responses[analysis_position].get_response_time_duration())
                ]
                analysis_string += ','.join(elements) + '\n'
                analysis_position += 1
        analysis_string += '\n' + str(number_of_successful_analysis) + ' of ' \
                           + str(len(self._requests)) + ' tests passed'
        return analysis_string
