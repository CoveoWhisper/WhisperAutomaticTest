import unittest
from datetime import timedelta

from whisper_automatic_test.exceptions.no_requests_exception import NoRequestsException
from whisper_automatic_test.exceptions.no_suggestions_responses_exception import NoSuggestionsResponsesException
from whisper_automatic_test.exceptions.no_suggestions_responses_for_every_requests_exception \
    import NoSuggestionsResponsesForEveryRequestsException
from whisper_automatic_test.request import Request
from whisper_automatic_test.scenario import Scenario
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file
from whisper_automatic_test.suggestion import Suggestion
from whisper_automatic_test.suggestions_response import SuggestionsResponse
from whisper_automatic_test.suggestions_responses_analyzer import SuggestionsResponsesAnalyzer
from whisper_automatic_test.whisper_api_adapter import whisper_response_to_suggestions

SCENARIO_FILE_PATH = 'test/resources/test_scenarios_for_suggestions_responses_analyzer.csv'
SCENARIOS_STARTING_WITH_SAME_FILE_PATH = 'test/resources/test_scenarios_second_scenario_starts_with_same.csv'
EXAMPLE_WHISPER_RESPONSE_FILE_PATH = 'test/resources/example_whisper_response_3_links.json'
EXAMPLE_WHISPER_RESPONSE_QUESTIONS_FILE_PATH = 'test/resources/example_whisper_response_3_questions.json'


def get_suggestions(file_path):
    with open(file_path) as file:
        return file.read()


class TestSuggestionsResponsesAnalyzer(unittest.TestCase):
    def setUp(self):
        self._scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        self._scenarios_starting_with_same = get_scenarios_from_csv_file(SCENARIOS_STARTING_WITH_SAME_FILE_PATH)

        suggestions_3_links = whisper_response_to_suggestions(get_suggestions(EXAMPLE_WHISPER_RESPONSE_FILE_PATH))
        suggestions_3_questions = whisper_response_to_suggestions(
            get_suggestions(EXAMPLE_WHISPER_RESPONSE_QUESTIONS_FILE_PATH)
        )
        suggestions_2_last_links = suggestions_3_links[1:]
        self._suggestions_responses_for_each_scenario = [
            [
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=49))
            ],
            [
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=49)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=49)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=49)),
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=54)),
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_2_last_links, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=48))
            ],
            [
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
                SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48))
            ]
        ]

        self._suggestions_responses_starting_with_same = [
            [
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=49))
            ],
            [
                SuggestionsResponse([], timedelta(seconds=49)),
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=49))
            ],
            [
                SuggestionsResponse(suggestions_3_links, timedelta(seconds=49))
            ]
        ]

    def test_constructor_with_no_request_in_scenarios(self):
        with self.assertRaises(NoRequestsException):
            SuggestionsResponsesAnalyzer([Scenario([])], self._suggestions_responses_for_each_scenario)

    def test_constructor_with_no_suggestions_responses(self):
        with self.assertRaises(NoSuggestionsResponsesException):
            SuggestionsResponsesAnalyzer(self._scenarios, [])

    def test_constructor_with_no_suggestions_response_for_every_request(self):
        with self.assertRaises(NoSuggestionsResponsesForEveryRequestsException):
            SuggestionsResponsesAnalyzer(self._scenarios, [SuggestionsResponse([], timedelta(seconds=10))])
        with self.assertRaises(NoSuggestionsResponsesForEveryRequestsException):
            suggestions_responses_for_each_scenario_but_not_good_size = [
                [
                    SuggestionsResponse([], timedelta(seconds=10))
                ],
                [
                    SuggestionsResponse([], timedelta(seconds=10))
                ],
                [
                    SuggestionsResponse([], timedelta(seconds=10))
                ],
            ]
            SuggestionsResponsesAnalyzer(self._scenarios, suggestions_responses_for_each_scenario_but_not_good_size)

    def test_analyze_with_one_successful_suggestions_response(self):
        expected_analysis = ['success(1-1)']
        request = Request('asker', 'What is Coveo?', 'link', 'https://www.coveo.com/')
        suggestion = Suggestion('link', 'https://www.coveo.com/')
        suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(
            [Scenario([request])],
            [[SuggestionsResponse([suggestion], timedelta(seconds=0))]])
        self.assertEquals(expected_analysis, suggestions_responses_analyzer.analyze_scenarios())

    def test_analyze(self):
        expected_analysis = [
            'fail',
            'success(1-1)',
            'success(1-1)',
            'success',
            'fail',
            'fail',
            'fail',
            'fail',
            'success',
            'fail',
            'fail',
            'success(1-2)',
            'success(1-2)',
            'fail',
            'fail',
            'fail',
            'fail',
            'success',
            'fail',
            'success',
            'fail'
        ]
        suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(
            self._scenarios,
            self._suggestions_responses_for_each_scenario
        )
        self.assertEquals(expected_analysis, suggestions_responses_analyzer.analyze_scenarios())

    def test_analyze_to_string(self):
        suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(
            self._scenarios,
            self._suggestions_responses_for_each_scenario
        )
        expected_analysis_string = \
            ('Scenario,Person,Message,Success condition,Result,System response time\n'
             '1,agent,I love mushrooms,same,fail,0:00:49\n'
             '2,asker,I have problems calling the rest API,link,success(1-1),0:00:49\n'
             '2,asker,I have problems calling the rest API,link,success(1-1),0:00:49\n'
             '2,agent,I love mushrooms,same,success,0:00:49\n'
             '2,asker,I have problems calling the rest API,link,fail,0:00:54\n'
             '2,asker,I have problems calling the rest API,link,fail,0:00:48\n'
             '2,asker,Should fail notlink success condition,notlink,fail,0:00:48\n'
             '2,asker,Should fail multiple unwanted links,notlink,fail,0:00:48\n'
             '2,agent,Should succeed notlink success condition,notlink,success,0:00:48\n'
             '2,agent,World,link,fail,0:00:48\n'
             '2,agent,World,link,fail,0:00:48\n'
             '3,asker,Hello,question,success(1-2),0:00:48\n'
             '3,asker,Hello,question,success(1-2),0:00:48\n'
             '3,asker,Hello,question,fail,0:00:48\n'
             '3,asker,Hello,question,fail,0:00:48\n'
             '3,asker,Hello,question,fail,0:00:48\n'
             '3,asker,Hello,question,fail,0:00:48\n'
             '3,asker,Hello,question,success,0:00:48\n'
             '3,asker,Hello,question,fail,0:00:48\n'
             '3,asker,Hello,link,success,0:00:48\n'
             '3,asker,Hello,link,fail,0:00:48\n'
             '\n8 of 21 tests passed')
        analysis_string = suggestions_responses_analyzer.analyze_to_string()
        self.assertEquals(expected_analysis_string, analysis_string)

    def test_same_at_start_of_scenario(self):
        expected_analysis_string = \
            ('Scenario,Person,Message,Success condition,Result,System response time\n'
             '1,agent,link required, should pass,link,success(1-1),0:00:49\n'
             '2,asker,same required, expects empty because start of scenario, should pass,same,success,0:00:49\n'
             '2,agent,link required, should pass,link,success(1-1),0:00:49\n'
             '3,asker,same required, expects empty because start of scenario, should fail,same,fail,0:00:49\n'
             '\n3 of 4 tests passed')
        suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(
            self._scenarios_starting_with_same,
            self._suggestions_responses_starting_with_same
        )
        analysis_string = suggestions_responses_analyzer.analyze_to_string()
        self.assertEquals(expected_analysis_string, analysis_string)
