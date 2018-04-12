import unittest

from whisper_automatic_test.metrics_analyzer import MetricsAnalyzer
from whisper_automatic_test.request import Request
from whisper_automatic_test.scenario import Scenario
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file
from whisper_automatic_test.suggestion import Suggestion
from whisper_automatic_test.suggestions_response import SuggestionsResponse
from whisper_automatic_test.whisper_api_adapter import whisper_response_to_suggestions

SCENARIO_FILE_PATH = 'test/resources/test_scenario.csv'
EXAMPLE_WHISPER_RESPONSE_FILE_PATH = 'test/resources/example_whisper_response.json'
EXAMPLE_WHISPER_RESPONSE_QUESTIONS_FILE_PATH = 'test/resources/example_whisper_response_questions.json'


def get_suggestions(file_path):
    with open(file_path) as file:
        return file.read()


class TestMetricsAnalyzer(unittest.TestCase):
    _metrics_analyzer = None

    @classmethod
    def setUpClass(cls):
        scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        suggestions_a = whisper_response_to_suggestions(get_suggestions(EXAMPLE_WHISPER_RESPONSE_FILE_PATH))
        suggestions_b = whisper_response_to_suggestions(get_suggestions(EXAMPLE_WHISPER_RESPONSE_QUESTIONS_FILE_PATH))
        suggestions_responses = [
            SuggestionsResponse(suggestions_a, 42, 91),
            SuggestionsResponse(suggestions_b, 42, 96),
            SuggestionsResponse(suggestions_b, 42, 90),
            SuggestionsResponse(suggestions_b, 42, 90),
            SuggestionsResponse(suggestions_a, 42, 90),
            SuggestionsResponse(suggestions_a, 42, 90),
        ]
        cls._metrics_analyzer = MetricsAnalyzer(scenarios, suggestions_responses)

    def test_calculate_average_system_response_time(self):
        self.assertAlmostEquals(49.167, self._metrics_analyzer.calculate_average_system_response_time(), places=3)

    def test_calculate_messages_number(self):
        metrics_analyzer = MetricsAnalyzer([Scenario([])], [SuggestionsResponse([], 10, 20)])
        self.assertEquals(0, metrics_analyzer.calculate_messages_number())
        self.assertEquals(6, self._metrics_analyzer.calculate_messages_number())

    def test_calculate_average_chosen_suggestion_position(self):
        self.assertEquals(1.5, self._metrics_analyzer.calculate_mean_position_of_chosen_suggestions())

    def test_calculate_total_number_of_suggestions_updates(self):
        self.assertEquals(3, self._metrics_analyzer.calculate_total_number_of_suggestions_updates())
        metrics_analyzer = MetricsAnalyzer(get_scenarios_from_csv_file(SCENARIO_FILE_PATH), [SuggestionsResponse([], 10, 20)])
        self.assertEquals(0, metrics_analyzer.calculate_total_number_of_suggestions_updates())

    def test_calculate_number_of_unwanted_suggestions_updates(self):
        self.assertEquals(1, self._metrics_analyzer.calculate_number_of_unwanted_suggestions_updates())
        metrics_analyzer = MetricsAnalyzer([Scenario([Request('asker', 'Hello', 'same', '')])], [SuggestionsResponse([Suggestion('link', 'www.hello.com')], 10, 20)])
        self.assertEquals(1, metrics_analyzer.calculate_total_number_of_suggestions_updates())

    def test_calculate_number_of_selected_suggestions(self):
        self.assertEquals(2, self._metrics_analyzer.calculate_number_of_selected_suggestions())

    def test_calculate_number_of_suggested_questions(self):
        self.assertEquals(6, self._metrics_analyzer.calculate_number_of_suggested_questions())

    def test_calculate_number_of_suggested_links(self):
        self.assertEquals(3, self._metrics_analyzer.calculate_number_of_suggested_links())

    def test_calculate_mean_confidence_level_of_selected_suggestions(self):
        self.assertEquals(0, self._metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions())
