from whisper_automatic_test.suggestions_response import SuggestionsResponse


class ScenariosRunner:
    _get_suggestions = None
    _get_time = None

    def __init__(self, get_suggestions, get_time):
        self._get_suggestions = get_suggestions
        self._get_time = get_time

    def run(self, scenarios):
        suggestions_responses_of_each_scenario = [
            self._get_suggestions_responses_of_scenario(scenario) for scenario in scenarios
        ]
        suggestions_responses_independent_of_the_scenario = sum(suggestions_responses_of_each_scenario, [])
        return suggestions_responses_independent_of_the_scenario

    def _get_suggestions_response_of_request(self, request):
        before_timestamp = self._get_time()
        suggestions = self._get_suggestions(request)
        after_timestamp = self._get_time()
        return SuggestionsResponse(suggestions, before_timestamp, after_timestamp)

    def _get_suggestions_responses_of_scenario(self, scenario):
        return [self._get_suggestions_response_of_request(request) for request in scenario.get_requests()]
