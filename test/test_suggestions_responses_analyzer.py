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
EXAMPLE_WHISPER_RESPONSE_FILE_PATH = 'test/resources/example_whisper_response_3_links.json'
EXAMPLE_WHISPER_RESPONSE_QUESTIONS_FILE_PATH = 'test/resources/example_whisper_response_3_questions.json'


def get_suggestions(file_path):
    with open(file_path) as file:
        return file.read()


class TestSuggestionsResponsesAnalyzer(unittest.TestCase):
    def setUp(self):
        self._scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        suggestions_3_links = whisper_response_to_suggestions(get_suggestions(EXAMPLE_WHISPER_RESPONSE_FILE_PATH))
        suggestions_3_questions = whisper_response_to_suggestions(
            get_suggestions(EXAMPLE_WHISPER_RESPONSE_QUESTIONS_FILE_PATH)
        )
        self._suggestions_responses = [
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=49)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=49)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=49)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=49)),
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=54)),
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_links, timedelta(seconds=48)),
            SuggestionsResponse(suggestions_3_questions, timedelta(seconds=48)),
        ]

    def test_constructor_with_no_request_in_scenarios(self):
        with self.assertRaises(NoRequestsException):
            SuggestionsResponsesAnalyzer([Scenario([])], self._suggestions_responses)

    def test_constructor_with_no_suggestions_responses(self):
        with self.assertRaises(NoSuggestionsResponsesException):
            SuggestionsResponsesAnalyzer(self._scenarios, [])

    def test_constructor_with_no_suggestions_response_for_every_request(self):
        with self.assertRaises(NoSuggestionsResponsesForEveryRequestsException):
            SuggestionsResponsesAnalyzer(self._scenarios, [SuggestionsResponse([], timedelta(seconds=10))])

    def test_analyze_with_one_successful_suggestions_response(self):
        expected_analysis = ['success(1)']
        request = Request('asker', 'What is Coveo?', 'link', 'https://www.coveo.com/')
        suggestion = Suggestion('link', 'https://www.coveo.com/')
        suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(
            [Scenario([request])],
            [SuggestionsResponse([suggestion], timedelta(seconds=0))])
        self.assertEquals(expected_analysis, suggestions_responses_analyzer.analyze())

    def test_analyze(self):
        expected_analysis = [
            'fail',
            'success(1)',
            'success(1)',
            'success',
            'fail',
            'fail',
            'fail',
            'fail',
            'success(2)',
            'success(2)',
            'fail',
            'fail',
            'fail',
            'fail',
            'success',
            'fail',
            'success',
            'fail'
        ]
        suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(self._scenarios, self._suggestions_responses)
        self.assertEquals(expected_analysis, suggestions_responses_analyzer.analyze())

    def test_analyze_to_string(self):
        suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(self._scenarios, self._suggestions_responses)
        expected_analysis_string = \
            ('1,agent,I love mushrooms,same,fail\n'
             '2,asker,I have problems calling the rest API,link,success(1)\n'
             '2,asker,I have problems calling the rest API,link,success(1)\n'
             '2,agent,I love mushrooms,same,success\n'
             '2,asker,I have problems calling the rest API,link,fail\n'
             '2,asker,I have problems calling the rest API,link,fail\n'
             '2,agent,World,link,fail\n'
             '2,agent,World,link,fail\n'
             '3,asker,Hello,question,success(2)\n'
             '3,asker,Hello,question,success(2)\n'
             '3,asker,Hello,question,fail\n'
             '3,asker,Hello,question,fail\n'
             '3,asker,Hello,question,fail\n'
             '3,asker,Hello,question,fail\n'
             '3,asker,Hello,question,success\n'
             '3,asker,Hello,question,fail\n'
             '3,asker,Hello,link,success\n'
             '3,asker,Hello,link,fail\n')
        analysis_string = suggestions_responses_analyzer.analyze_to_string()
        self.assertEquals(expected_analysis_string, analysis_string)
