import unittest

from whisper_automatic_test.metrics_analyzer import MetricsAnalyzer
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file
from whisper_automatic_test.suggestions_response import SuggestionsResponse
from whisper_automatic_test.whisper_api_adapter import whisper_response_to_suggestions

SCENARIO_FILE_PATH = 'test/resources/test_scenario.csv'
EXAMPLE_WHISPER_RESPONSE_FILE_PATH = 'test/resources/example_whisper_response.json'
EXAMPLE_WHISPER_RESPONSE_QUESTIONS_FILE_PATH = 'test/resources/example_whisper_response_questions.json'


def get_suggestions(file_path):
    with open(file_path) as file:
        return file.read()


class TestMetricsAnalyzer(unittest.TestCase):
    metrics_analyzer = None

    @classmethod
    def setUpClass(cls):
        scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        suggestions_a = whisper_response_to_suggestions(get_suggestions(EXAMPLE_WHISPER_RESPONSE_FILE_PATH))
        suggestions_b = whisper_response_to_suggestions(get_suggestions(EXAMPLE_WHISPER_RESPONSE_QUESTIONS_FILE_PATH))
        suggestions_responses = [
            SuggestionsResponse(suggestions_a, 42, 90),
            SuggestionsResponse(suggestions_b, 42, 93),
            SuggestionsResponse(suggestions_b, 42, 90)
        ]
        cls._metrics_analyzer = MetricsAnalyzer(scenarios, suggestions_responses)

    def test_average_system_response_time(self):
        self.assertEquals(49, self._metrics_analyzer.calculate_average_system_response_time())

    def test_messages_number(self):
        self.assertEquals(3, self._metrics_analyzer.calculate_messages_number())

    def test_average_chosen_suggestion_position(self):
        self.assertEquals(2, self._metrics_analyzer.calculate_average_chosen_suggestion_position())
