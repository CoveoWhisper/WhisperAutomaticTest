import unittest

from whisper_automatic_test.metrics_analyzer import MetricsAnalyzer
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file
from whisper_automatic_test.suggestions_response import SuggestionsResponse
from whisper_automatic_test.whisper_api_adapter import whisper_response_to_suggestions

SCENARIO_FILE_PATH = 'test/resources/test_scenario.csv'
EXAMPLE_WHISPER_RESPONSE_FILE_PATH = 'test/resources/example_whisper_response.json'


class TestMetricsAnalyzer(unittest.TestCase):
    _metrics_analyzer = None

    def setUp(self):
        scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        with open(EXAMPLE_WHISPER_RESPONSE_FILE_PATH) as file:
            example_whisper_response = file.read()
        suggestions = whisper_response_to_suggestions(example_whisper_response)
        suggestions_responses = [
            SuggestionsResponse(suggestions, 42, 90),
            SuggestionsResponse(suggestions, 42, 92)
        ]
        self._metrics_analyzer = MetricsAnalyzer(scenarios, suggestions_responses)

    def test_average_system_response_time(self):
        self.assertEquals(49, self._metrics_analyzer.calculate_average_system_response_time())

    def test_messages_number(self):
        self.setUp()
        self.assertEquals(3, self._metrics_analyzer.calculate_messages_number())
