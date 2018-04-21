import uuid

from whisper_automatic_test.suggestions_response import SuggestionsResponse


class ScenariosRunner:
    _get_suggestions = None
    _get_time = None

    def __init__(self, get_suggestions, get_time):
        self._get_suggestions = get_suggestions
        self._get_time = get_time

    def run(self, scenarios):
        scenario_chatkey_pairs = [(scenario, str(uuid.uuid4())) for scenario in scenarios]
        suggestions_responses_of_each_scenario = [
            self._get_suggestions_responses_of_scenario(scenario_chatkey_pair[0], scenario_chatkey_pair[1])
            for scenario_chatkey_pair in scenario_chatkey_pairs
        ]
        return suggestions_responses_of_each_scenario

    def _get_suggestions_response_of_request(self, request, chatkey):
        before_datetime = self._get_time()
        suggestions = self._get_suggestions(request, chatkey)
        after_datetime = self._get_time()
        return SuggestionsResponse(suggestions, after_datetime - before_datetime)

    def _get_suggestions_responses_of_scenario(self, scenario, chatkey):
        return [self._get_suggestions_response_of_request(request, chatkey) for request in scenario.get_requests()]
