import unittest
from datetime import timedelta, datetime
from unittest.mock import Mock

from whisper_automatic_test.request import Request
from whisper_automatic_test.scenario import Scenario
from whisper_automatic_test.scenarios_runner import ScenariosRunner
from whisper_automatic_test.suggestion import Suggestion


class TestScenariosRunner(unittest.TestCase):

    def setUp(self):
        self._scenarios = [
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

        self._mock_get_suggestions = Mock()
        self._mock_get_suggestions.side_effect = [
            [Suggestion('link', 'some_url'), Suggestion('link', 'another_url')],
            [Suggestion('link', 'url_of_a_different_suggestions_response')],
            [Suggestion('link', 'some_url_of_suggestion_scenario_2')]
        ]

        self._mock_get_time = Mock()
        self._mock_get_time.side_effect = [
            datetime(2005, 12, 30, 6, 45, 1),
            datetime(2005, 12, 30, 6, 45, 2),
            datetime(2005, 12, 30, 6, 45, 4),
            datetime(2005, 12, 30, 6, 45, 7),
            datetime(2005, 12, 30, 6, 45, 11),
            datetime(2005, 12, 30, 6, 45, 16)
        ]

        self._scenario_runner = ScenariosRunner(self._mock_get_suggestions, self._mock_get_time)

    def test_run_scenarios(self):
        suggestions_responses_of_each_scenario = self._scenario_runner.run(self._scenarios)
        self.assertEquals(2, len(suggestions_responses_of_each_scenario))

        suggestions_responses_of_scenario_a = suggestions_responses_of_each_scenario[0]
        suggestions_responses_of_scenario_b = suggestions_responses_of_each_scenario[1]
        self.assertEquals(2, len(suggestions_responses_of_scenario_a))
        self.assertEquals(1, len(suggestions_responses_of_scenario_b))

        suggestions_reponse_a = suggestions_responses_of_scenario_a[0]
        suggestions_reponse_b = suggestions_responses_of_scenario_a[1]
        suggestions_reponse_c = suggestions_responses_of_scenario_b[0]

        suggestions_a = suggestions_reponse_a.get_suggestions()
        self.assertEquals(2, len(suggestions_a))
        self.assertEquals('link', suggestions_a[0].get_type())
        self.assertEquals('some_url', suggestions_a[0].get_data())
        self.assertEquals('link', suggestions_a[1].get_type())
        self.assertEquals('another_url', suggestions_a[1].get_data())
        self.assertEquals(timedelta(seconds=1), suggestions_reponse_a.get_response_time_duration())

        suggestions_b = suggestions_reponse_b.get_suggestions()
        self.assertEquals(1, len(suggestions_b))
        self.assertEquals('link', suggestions_b[0].get_type())
        self.assertEquals('url_of_a_different_suggestions_response', suggestions_b[0].get_data())
        self.assertEquals(timedelta(seconds=3), suggestions_reponse_b.get_response_time_duration())

        suggestions_c = suggestions_reponse_c.get_suggestions()
        self.assertEquals(1, len(suggestions_c))
        self.assertEquals('link', suggestions_c[0].get_type())
        self.assertEquals('some_url_of_suggestion_scenario_2', suggestions_c[0].get_data())
        self.assertEquals(timedelta(seconds=5), suggestions_reponse_c.get_response_time_duration())

    def test_run_each_scenario_with_unique_chatkey(self):
        self._scenario_runner.run(self._scenarios)

        calls = self._mock_get_suggestions.call_args_list
        first_call = calls[0][0]
        first_request = first_call[0]
        first_chatkey = first_call[1]
        self.assertEquals('asker', first_request.get_person())
        self.assertEquals('hello', first_request.get_message())
        self.assertEquals('link', first_request.get_success_condition())
        self.assertEquals(['https://some_link.com'], first_request.get_data())

        second_call = calls[1][0]
        second_chatkey = second_call[1]

        third_call = calls[2][0]
        third_chatkey = third_call[1]

        self.assertEquals(first_chatkey, second_chatkey)
        self.assertNotEquals(first_chatkey, third_chatkey)
