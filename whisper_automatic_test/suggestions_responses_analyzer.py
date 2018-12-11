from whisper_automatic_test.exceptions.no_requests_exception import NoRequestsException
from whisper_automatic_test.exceptions.no_suggestions_responses_exception import NoSuggestionsResponsesException
from whisper_automatic_test.exceptions.no_suggestions_responses_for_every_requests_exception \
    import NoSuggestionsResponsesForEveryRequestsException
from whisper_automatic_test.utility import raise_if_there_is_no_request_in_scenarios, \
    raise_if_there_is_no_suggestions_responses, raise_if_there_is_not_a_suggestions_response_for_every_request, \
    get_requests


def get_first_question(suggestions):
    for suggestion in suggestions:
        if suggestion.get_type() == "question":
            return [1, suggestion]
    return None


def get_first_non_forbidden_link(suggestions, forbidden_links):
    suggested_links = [suggestion for suggestion in suggestions if suggestion.get_type() == "link"]
    for i, suggested_link in enumerate(suggested_links):
        is_acceptable_link = True
        for forbidden_link in forbidden_links:
            if suggested_link.get_data() == forbidden_link:
                is_acceptable_link = False;
                break
        if is_acceptable_link:
            return [i + 1, suggested_link]
    return None


def get_first_matching_link(suggestions, acceptable_links):
    suggested_links = [suggestion for suggestion in suggestions if suggestion.get_type() == "link"]
    for i, suggested_link in enumerate(suggested_links):
        for acceptable_link in acceptable_links:
            if safe_str_lower(suggested_link.get_data()) == safe_str_lower(acceptable_link):
                return [i + 1, suggested_link]
    return None


def safe_str_lower(url):
    if url:
        return url.lower()

    return None

def get_selected_suggestion(suggestions, request):
    success_condition = request.get_success_condition()
    if success_condition == "question":
        return get_first_question(suggestions)
    if success_condition == "link":
        return get_first_matching_link(suggestions, request.get_data())
    if success_condition == "notlink":
        return get_first_non_forbidden_link(suggestions, request.get_data())
    return None


def get_selected_suggestions(suggestions_responses, requests):
    selected_suggestions = []
    for i, suggestions_response in enumerate(suggestions_responses):
        request = requests[i]
        suggestions = suggestions_response.get_suggestions()
        selected_suggestion = get_selected_suggestion(
            suggestions,
            request)
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
    is_link_or_question = (
            request.get_success_condition() == 'link' or
            request.get_success_condition() == 'question'
    )
    has_no_data = not request.get_data()
    is_valid_link_or_question_request = is_link_or_question and has_no_data
    if not is_valid_link_or_question_request:
        return False
    for suggestion in suggestions:
        if request.get_success_condition() == suggestion.get_type():
            return True
    return False


def analyse_notlink_with_request_data(request, current_suggestions):
    is_valid_request = (
            request.get_success_condition() == 'notlink' and
            request.get_data()
    )
    if not is_valid_request:
        return False
    forbidden_links = request.get_data()
    suggested_links = [suggestion.get_data() for suggestion in current_suggestions]
    forbidden_suggested_links = set(forbidden_links).intersection(set(suggested_links))
    return 0 == len(forbidden_suggested_links)


def analyze_scenario(scenario, suggestions_responses_for_current_scenario):
    analysis = []
    previous_suggestions = []
    for i, request in enumerate(scenario.get_requests()):
        suggestions_reponse_of_request = suggestions_responses_for_current_scenario[i]
        suggestions_for_request = suggestions_reponse_of_request.get_suggestions()
        is_success = analyse_same(request, suggestions_for_request, previous_suggestions)
        is_success |= analyse_link_or_question_without_request_data(request, suggestions_for_request)
        is_success |= analyse_notlink_with_request_data(request, suggestions_for_request)
        if is_success:
            analysis.append('success')
        else:
            selected_suggestion_position = analyse_link_or_question_with_request_data(request, suggestions_for_request)
            analysis.append('success(' + selected_suggestion_position + ')') if selected_suggestion_position \
                else analysis.append('fail')
        previous_suggestions = suggestions_for_request
    return analysis


class SuggestionsResponsesAnalyzer:
    def __init__(self, scenarios, suggestions_responses_for_each_scenario):
        self._scenarios = scenarios
        self._suggestions_responses_for_each_scenario = suggestions_responses_for_each_scenario
        raise_if_there_is_no_request_in_scenarios(scenarios)
        raise_if_there_is_no_suggestions_responses(suggestions_responses_for_each_scenario)
        raise_if_there_is_not_a_suggestions_response_for_every_request(
            scenarios,
            suggestions_responses_for_each_scenario
        )

    def raise_if_there_is_no_request_in_scenarios(self):
        if not get_requests(self._scenarios):
            raise NoRequestsException('No requests')

    def raise_if_there_is_no_suggestions_responses(self):
        if not self._suggestions_responses_for_each_scenario:
            raise NoSuggestionsResponsesException('No suggestions responses to analyze')

    def raise_if_there_is_not_a_suggestions_response_for_every_request(self):
        no_suggestions_responses_for_every_request_exception = NoSuggestionsResponsesForEveryRequestsException(
            'There is not a suggestions response for every request')
        if len(self._scenarios) != len(self._suggestions_responses_for_each_scenario):
            raise no_suggestions_responses_for_every_request_exception
        for i, scenario in enumerate(self._scenarios):
            suggestions_responses_for_scenario = self._suggestions_responses_for_each_scenario[i]
            if len(scenario.get_requests()) != len(suggestions_responses_for_scenario):
                raise no_suggestions_responses_for_every_request_exception

    def analyze_scenarios(self):
        analysis = []
        for i, scenario in enumerate(self._scenarios):
            suggestions_responses_for_current_scenario = self._suggestions_responses_for_each_scenario[i]
            for scenario_analysis in analyze_scenario(scenario, suggestions_responses_for_current_scenario):
                analysis.append(scenario_analysis)
        return analysis

    def analyze_to_string(self):
        analysis = self.analyze_scenarios()
        number_of_successful_analysis = sum(['success' in single_analysis for single_analysis in analysis])
        analysis_position = 0
        analysis_string = 'Request,Scenario,Person,Message,Success condition,Result,System response time\n'
        for i, scenario in enumerate(self._scenarios):
            suggestions_responses_scenario = self._suggestions_responses_for_each_scenario[i]
            for j, request in enumerate(scenario.get_requests()):
                scenario_id = str(i + 1)
                elements = [
                    str(analysis_position),
                    scenario_id,
                    request.get_person(),
                    request.get_message(),
                    request.get_success_condition(),
                    analysis[analysis_position],
                    str(suggestions_responses_scenario[j].get_response_time_duration())
                ]
                analysis_string += ','.join(elements) + '\n'
                analysis_position += 1
        analysis_string += '\n' + str(number_of_successful_analysis) + ' of ' \
                           + str(len(get_requests(self._scenarios))) + ' tests passed'
        return analysis_string
