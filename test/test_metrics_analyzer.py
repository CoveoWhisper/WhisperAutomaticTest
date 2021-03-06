import math
import unittest
from datetime import timedelta

from whisper_automatic_test.exceptions.invalid_timestamp_exception import InvalidTimestampException
from whisper_automatic_test.exceptions.no_requests_exception import NoRequestsException
from whisper_automatic_test.exceptions.no_suggestions_responses_exception import NoSuggestionsResponsesException
from whisper_automatic_test.exceptions.no_suggestions_responses_for_every_requests_exception import \
    NoSuggestionsResponsesForEveryRequestsException
from whisper_automatic_test.metrics_analyzer import MetricsAnalyzer
from whisper_automatic_test.request import Request
from whisper_automatic_test.scenario import Scenario
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file
from whisper_automatic_test.suggestion import Suggestion
from whisper_automatic_test.suggestions_response import SuggestionsResponse

SCENARIO_FILE_PATH = 'test/resources/scenarios_csv/test_scenarios_for_metrics.csv'


def get_suggestions(file_path):
    with open(file_path) as file:
        return file.read()


class TestMetricsAnalyzer(unittest.TestCase):
    def setUp(self):
        self._suggestions_3_links = [
            Suggestion('link', 'https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/'),
            Suggestion('link', 'https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html'),
            Suggestion('link', 'https://onlinehelp.coveo.com/en/ces/7.0/administrator/about_net_conversion_scripts.htm')
        ]
        self._suggestions_3_questions = [
            Suggestion('question', 'What is your name?'),
            Suggestion('question', 'Did you try this?'),
            Suggestion('question', 'Hello?')
        ]
        suggestions_responses_for_each_scenario = [
            [
                SuggestionsResponse(self._suggestions_3_questions, timedelta(seconds=49)),
                SuggestionsResponse(self._suggestions_3_links, timedelta(seconds=49))
            ],
            [
                SuggestionsResponse(self._suggestions_3_questions, timedelta(seconds=54)),
                SuggestionsResponse(self._suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(self._suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(self._suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(self._suggestions_3_links, timedelta(seconds=48))
            ]
        ]
        self._scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        self._metrics_analyzer = MetricsAnalyzer(self._scenarios, suggestions_responses_for_each_scenario)
        empty_suggestions_suggestions_responses_for_each_scenario = [
            [
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=0))
            ],
            [
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=0))
            ]
        ]
        self._no_suggestions_responses_metrics_analyzer = \
            MetricsAnalyzer(self._scenarios, empty_suggestions_suggestions_responses_for_each_scenario)
        self._immediate_response_metrics_analyzer = \
            MetricsAnalyzer(self._scenarios, empty_suggestions_suggestions_responses_for_each_scenario)

    def test_constructor_with_no_request_in_scenarios(self):
        with self.assertRaises(NoRequestsException):
            MetricsAnalyzer([Scenario([])], [[SuggestionsResponse([], timedelta(seconds=10))]])

    def test_constructor_with_no_suggestions_responses(self):
        with self.assertRaises(NoSuggestionsResponsesException):
            MetricsAnalyzer(self._scenarios, [])

    def test_constructor_with_invalid_response_timestamp(self):
        invalid_timestamp_suggestions_responses_for_each_scenario = [
            [
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=0))
            ],
            [
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=-666)),
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=0)),
                SuggestionsResponse([], timedelta(seconds=0))
            ]
        ]
        with self.assertRaises(InvalidTimestampException):
            MetricsAnalyzer(self._scenarios, invalid_timestamp_suggestions_responses_for_each_scenario)

    def test_constructor_with_no_suggestions_response_for_every_request(self):
        with self.assertRaises(NoSuggestionsResponsesForEveryRequestsException):
            MetricsAnalyzer(self._scenarios, [[SuggestionsResponse([], timedelta(seconds=10))]])

    def test_average_system_response_time(self):
        actual = self._metrics_analyzer.calculate_average_system_response_time()
        expected = timedelta(seconds=49.143)
        self.assertAlmostEquals(expected, actual, delta=timedelta(seconds=0.001))

    def test_average_system_response_time_with_immediate_response(self):
        self.assertAlmostEquals(
            timedelta(seconds=0),
            self._immediate_response_metrics_analyzer.calculate_average_system_response_time()
        )

    def test_messages_number(self):
        self.assertEquals(7, self._metrics_analyzer.calculate_messages_number())

    def test_average_selected_suggestion_position(self):
        self.assertEquals(1, self._metrics_analyzer.calculate_mean_position_of_selected_suggestions())

    def test_average_selected_suggestion_position_when_no_suggestion_is_selected(self):
        self.assertEquals(
            math.inf,
            self._no_suggestions_responses_metrics_analyzer.calculate_mean_position_of_selected_suggestions()
        )

    def test_average_selected_suggestion_position_only_counts_questions_when_expecting_questions(self):
        suggestions = [
            Suggestion('link', 'dummy_urlA'),
            Suggestion('link', 'dummy_urlB'),
            Suggestion('link', 'dummy_urlC'),
            Suggestion('question', 'dummy_questionA'),
            Suggestion('question', 'dummy_questionB'),
            Suggestion('question', 'dummy_questionC')
        ]
        request = Request(
            None,
            None,
            "question",
            ""
        )
        scenarios = [Scenario([request])]
        suggestions_responses_for_each_scenario = [[
            SuggestionsResponse(
                suggestions,
                timedelta(seconds=42)
            )
        ]]
        metrics_analyzer = MetricsAnalyzer(scenarios, suggestions_responses_for_each_scenario)
        self.assertEquals(1, metrics_analyzer.calculate_mean_position_of_selected_suggestions())

    def test_total_number_of_suggestions_updates(self):
        self.assertEquals(4, self._metrics_analyzer.calculate_total_number_of_suggestions_updates())

    def test_total_number_of_suggestions_updates_with_no_suggestions_updates(self):
        self.assertEquals(
            0,
            self._no_suggestions_responses_metrics_analyzer.calculate_total_number_of_suggestions_updates()
        )

    def test_number_of_unwanted_suggestions_updates(self):
        self.assertEquals(
            2,
            self._metrics_analyzer.calculate_number_of_unwanted_suggestions_updates()
        )

    def test_number_of_unwanted_suggestions_updates_when_no_suggestions_update(self):
        self.assertEquals(
            0,
            self._no_suggestions_responses_metrics_analyzer.calculate_number_of_unwanted_suggestions_updates()
        )

    def test_number_of_selected_suggestions(self):
        self.assertEquals(2, self._metrics_analyzer.calculate_number_of_selected_suggestions())

    def test_number_of_selected_suggestions_when_there_are_none(self):
        self.assertEquals(0, self._no_suggestions_responses_metrics_analyzer.calculate_number_of_selected_suggestions())

    def test_number_of_suggested_questions(self):
        self.assertEquals(6, self._metrics_analyzer.calculate_number_of_suggested_questions())

    def test_number_of_suggested_questions_with_no_suggestions_responses(self):
        self.assertEquals(0, self._no_suggestions_responses_metrics_analyzer.calculate_number_of_suggested_questions())

    def test_number_of_suggested_questions_when_not_all_questions_updated(self):
        suggestions_responses_for_each_scenario = [
            [
                SuggestionsResponse(self._suggestions_3_links, timedelta(seconds=49)),
                SuggestionsResponse(self._suggestions_3_questions, timedelta(seconds=49))
            ],
            [
                SuggestionsResponse(self._suggestions_3_links, timedelta(seconds=54)),
                SuggestionsResponse(self._suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(self._suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(self._suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(self._suggestions_3_questions, timedelta(seconds=48))
            ]
        ]
        metrics_analyzer = MetricsAnalyzer(self._scenarios, suggestions_responses_for_each_scenario)
        self.assertEquals(6, metrics_analyzer.calculate_number_of_suggested_questions())

    def test_number_of_suggested_links(self):
        self.assertEquals(6, self._metrics_analyzer.calculate_number_of_suggested_links())

    def test_mean_confidence_level_of_selected_suggestions(self):
        self.assertEquals(0, self._metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions())
