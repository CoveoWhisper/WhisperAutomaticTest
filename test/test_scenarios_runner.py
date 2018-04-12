import unittest
from unittest.mock import Mock

from whisper_automatic_test.request import Request
from whisper_automatic_test.scenario import Scenario
from whisper_automatic_test.scenarios_runner import ScenariosRunner
from whisper_automatic_test.suggestion import Suggestion


class TestScenariosRunner(unittest.TestCase):
    def test_run_scenarios(self):
        scenarios = [
            Scenario(
                [
                    Request('asker', 'hello', 'link', 'https://some_link.com'),
                    Request('agent', 'world', 'same', ''),
                ]
            ),
            Scenario(
                [
                    Request('asker', 'question_scenario_2', 'link', 'some_url_scenario_2'),
                ]
            )
        ]

        mock_get_suggestions = Mock()
        mock_get_suggestions.side_effect = [
            [Suggestion('link', 'some_url'), Suggestion('link', 'another_url')],
            [Suggestion('link', 'url_of_a_different_suggestions_response')],
            [Suggestion('link', 'some_url_of_suggestion_scenario_2')]
        ]

        mock_get_time = Mock()
        mock_get_time.side_effect = [11, 22, 33, 44, 55, 66]

        scenario_runner = ScenariosRunner(mock_get_suggestions, mock_get_time)
        suggestions_responses = scenario_runner.run(scenarios)
        self.assertEquals(3, len(suggestions_responses))
        suggestions_a = suggestions_responses[0].get_suggestions()
        self.assertEquals(2, len(suggestions_a))
        self.assertEquals('link', suggestions_a[0].get_type())
        self.assertEquals('some_url', suggestions_a[0].get_data())
        self.assertEquals('link', suggestions_a[1].get_type())
        self.assertEquals('another_url', suggestions_a[1].get_data())
        self.assertEquals(11, suggestions_responses[0].get_timestamp_sent_request())
        self.assertEquals(22, suggestions_responses[0].get_timestamp_received_response())

        suggestions_b = suggestions_responses[1].get_suggestions()
        self.assertEquals(1, len(suggestions_b))
        self.assertEquals('link', suggestions_b[0].get_type())
        self.assertEquals('url_of_a_different_suggestions_response', suggestions_b[0].get_data())
        self.assertEquals(33, suggestions_responses[1].get_timestamp_sent_request())
        self.assertEquals(44, suggestions_responses[1].get_timestamp_received_response())

        suggestions_c = suggestions_responses[2].get_suggestions()
        self.assertEquals(1, len(suggestions_c))
        self.assertEquals('link', suggestions_c[0].get_type())
        self.assertEquals('some_url_of_suggestion_scenario_2', suggestions_c[0].get_data())
        self.assertEquals(55, suggestions_responses[2].get_timestamp_sent_request())
        self.assertEquals(66, suggestions_responses[2].get_timestamp_received_response())
