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
from whisper_automatic_test.suggestions_responses_analyzer import SuggestionsResponsesAnalyzer, get_selected_suggestion, \
    analyse_notlink_with_request_data, analyse_same, analyse_link_or_question_with_request_data, \
    analyse_link_or_question_without_request_data

SCENARIO_FILE_PATH = 'test/resources/scenarios_csv/test_scenarios_for_suggestions_responses_analyzer.csv'
SCENARIOS_STARTING_WITH_SAME_FILE_PATH = \
    'test/resources/scenarios_csv/test_scenarios_second_scenario_starts_with_same.csv'


def get_suggestions(file_path):
    with open(file_path) as file:
        return file.read()


class TestSuggestionsResponsesAnalyzer(unittest.TestCase):
    def setUp(self):
        self._scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        self._scenarios_starting_with_same = get_scenarios_from_csv_file(SCENARIOS_STARTING_WITH_SAME_FILE_PATH)

        suggestions_3_links = [
            Suggestion('link', 'https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/'),
            Suggestion('link', 'https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html'),
            Suggestion('link', 'https://onlinehelp.coveo.com/en/ces/7.0/administrator/about_net_conversion_scripts.htm')
        ]
        suggestions_3_questions = [
            Suggestion('question', 'What is your name?'),
            Suggestion('question', 'Did you try this?'),
            Suggestion('question', 'Hello?')
        ]
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
            ('Request,Scenario,Person,Message,Success condition,Result,System response time\n'
             '0,1,agent,I love mushrooms,same,fail,0:00:49\n'
             '1,2,asker,I have problems calling the rest API,link,success(1-1),0:00:49\n'
             '2,2,asker,I have problems calling the rest API,link,success(1-1),0:00:49\n'
             '3,2,agent,I love mushrooms,same,success,0:00:49\n'
             '4,2,asker,I have problems calling the rest API,link,fail,0:00:54\n'
             '5,2,asker,I have problems calling the rest API,link,fail,0:00:48\n'
             '6,2,asker,Should fail notlink success condition,notlink,fail,0:00:48\n'
             '7,2,asker,Should fail multiple unwanted links,notlink,fail,0:00:48\n'
             '8,2,agent,Should succeed notlink success condition,notlink,success,0:00:48\n'
             '9,2,agent,World,link,fail,0:00:48\n'
             '10,2,agent,World,link,fail,0:00:48\n'
             '11,3,asker,Hello,question,success(1-2),0:00:48\n'
             '12,3,asker,Hello,question,success(1-2),0:00:48\n'
             '13,3,asker,Hello,question,fail,0:00:48\n'
             '14,3,asker,Hello,question,fail,0:00:48\n'
             '15,3,asker,Hello,question,fail,0:00:48\n'
             '16,3,asker,Hello,question,fail,0:00:48\n'
             '17,3,asker,Hello,question,success,0:00:48\n'
             '18,3,asker,Hello,question,fail,0:00:48\n'
             '19,3,asker,Hello,link,success,0:00:48\n'
             '20,3,asker,Hello,link,fail,0:00:48\n'
             '\n8 of 21 tests passed')
        analysis_string = suggestions_responses_analyzer.analyze_to_string()
        self.assertEquals(expected_analysis_string, analysis_string)

    def test_same_at_start_of_scenario(self):
        expected_analysis_string = \
            ('Request,Scenario,Person,Message,Success condition,Result,System response time\n'
             '0,1,agent,link required, should pass,link,success(1-1),0:00:49\n'
             '1,2,asker,same required, expects empty because start of scenario, should pass,same,success,0:00:49\n'
             '2,2,agent,link required, should pass,link,success(1-1),0:00:49\n'
             '3,3,asker,same required, expects empty because start of scenario, should fail,same,fail,0:00:49\n'
             '\n3 of 4 tests passed')
        suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(
            self._scenarios_starting_with_same,
            self._suggestions_responses_starting_with_same
        )
        analysis_string = suggestions_responses_analyzer.analyze_to_string()
        self.assertEquals(expected_analysis_string, analysis_string)

    def test_when_found_then_get_selected_suggestion_returns_matching_suggestion(self):
        suggestions = [
            Suggestion(
                "link",
                "some_dummy_url"
            ),
            Suggestion(
                "link",
                "some_expected_url"
            ),
            Suggestion(
                "link",
                "another_dummy_url"
            )
        ]
        request = Request(
            None,
            None,
            "link",
            "some_expected_url"
        )
        actual_selected_suggestion = get_selected_suggestion(
            suggestions,
            request
        )
        self.assertIsNotNone(actual_selected_suggestion)
        self.assertEquals(2, actual_selected_suggestion[0])
        self.assertEquals(
            Suggestion(
                "link",
                "some_expected_url"
            ),
            actual_selected_suggestion[1]
        )

    def test_when_expected_question_then_get_selected_suggestion_returns_the_first_question(self):
        suggestions = [
            Suggestion(
                "link",
                "some_dummy_url"
            ),
            Suggestion(
                "question",
                "some_question_data"
            ),
            Suggestion(
                "link",
                "another_dummy_url"
            )
        ]
        request = Request(
            None,
            None,
            "question",
            ""
        )
        selected_suggestion = get_selected_suggestion(
            suggestions,
            request
        )
        self.assertIsNotNone(selected_suggestion)
        self.assertEquals(2, selected_suggestion[0])
        self.assertEquals(
            Suggestion(
                "question",
                "some_question_data"
            ),
            selected_suggestion[1]
        )

    def test_when_not_found_then_get_selected_suggestion_returns_none(self):
        suggestions = [
            Suggestion(
                "link",
                "some_dummy_url"
            ),
            Suggestion(
                "link",
                "more_dummy_url"
            ),
            Suggestion(
                "link",
                "another_dummy_url"
            )
        ]
        request = Request(
            None,
            None,
            "link",
            "some_expected_url"
        )
        actual_selected_suggestion = get_selected_suggestion(
            suggestions,
            request
        )
        self.assertIsNone(actual_selected_suggestion)

    def test_pass_when_expected_notlink_and_suggestion_does_not_contain_the_forbidden_link(self):
        request = Request(
            None,
            None,
            "notlink",
            "url_not_in_the_suggestions"
        )
        suggestions = [
            Suggestion(
                "link",
                "urlA"
            ),
            Suggestion(
                "link",
                "urlB"
            ),
            Suggestion(
                "link",
                "urlC"
            )
        ]
        self.assertTrue(analyse_notlink_with_request_data(request, suggestions))

    def test_fail_when_expected_notlink_and_suggestion_contains_the_forbidden_link(self):
        request = Request(
            None,
            None,
            "notlink",
            "forbidden_url"
        )
        suggestions = [
            Suggestion(
                "link",
                "urlA"
            ),
            Suggestion(
                "link",
                "forbidden_url"
            ),
            Suggestion(
                "link",
                "urlC"
            )
        ]
        self.assertFalse(analyse_notlink_with_request_data(request, suggestions))

    def test_fail_when_expected_notlink_and_suggestion_contains_even_just_one_forbidden_link(self):
        request = Request(
            None,
            None,
            "notlink",
            "forbidden_urlA forbidden_urlB"
        )
        suggestions = [
            Suggestion(
                "link",
                "urlA"
            ),
            Suggestion(
                "link",
                "forbidden_urlB"
            ),
            Suggestion(
                "link",
                "urlC"
            )
        ]
        self.assertFalse(analyse_notlink_with_request_data(request, suggestions))

    def test_pass_when_expected_same_and_suggestions_are_the_same(self):
        request = Request(
            None,
            None,
            "same",
            ""
        )
        previous_suggestions = [
            Suggestion(
                "link",
                "urlA"
            ),
            Suggestion(
                "question",
                "question_data"
            )
        ]
        current_suggestions = [
            Suggestion(
                "link",
                "urlA"
            ),
            Suggestion(
                "question",
                "question_data"
            )
        ]
        self.assertTrue(analyse_same(request, current_suggestions, previous_suggestions))

    def test_fail_when_expected_same_and_suggestions_are_different(self):
        request = Request(
            None,
            None,
            "same",
            ""
        )
        previous_suggestions = [
            Suggestion(
                "link",
                "urlA"
            ),
            Suggestion(
                "question",
                "question_data"
            )
        ]
        current_suggestions = [
            Suggestion(
                "link",
                "different_url"
            ),
            Suggestion(
                "question",
                "question_data"
            )
        ]
        self.assertFalse(analyse_same(request, current_suggestions, previous_suggestions))

    def test_pass_when_expected_link_and_one_suggestion_contains_the_link(self):
        request = Request(
            None,
            None,
            "link",
            "expected_link"
        )
        suggestions = [
            Suggestion(
                "link",
                "expected_link"
            ),
            Suggestion(
                "question",
                "question_data"
            )
        ]
        self.assertTrue(analyse_link_or_question_with_request_data(request, suggestions))

    def test_fail_when_expected_link_and_no_suggestion_contains_the_link(self):
        request = Request(
            None,
            None,
            "link",
            "expected_link"
        )
        suggestions = [
            Suggestion(
                "link",
                "not_the_expected_link"
            ),
            Suggestion(
                "question",
                "question_data"
            )
        ]
        self.assertFalse(analyse_link_or_question_with_request_data(request, suggestions))

    def test_fail_when_expected_link_and_no_suggestion_contains_the_link(self):
        request = Request(
            None,
            None,
            "link",
            "expected_link"
        )
        suggestions = [
            Suggestion(
                "link",
                "not_the_expected_link"
            ),
            Suggestion(
                "question",
                "question_data"
            )
        ]
        self.assertFalse(analyse_link_or_question_with_request_data(request, suggestions))

    def test_pass_when_expected_question_and_one_suggestion_is_a_question(self):
        request = Request(
            None,
            None,
            "question",
            ""
        )
        suggestions = [
            Suggestion(
                "link",
                "someLink"
            ),
            Suggestion(
                "question",
                "question_data"
            )
        ]
        self.assertTrue(analyse_link_or_question_without_request_data(request, suggestions))

    def test_fail_when_expected_question_and_no_suggestion_is_a_question(self):
        request = Request(
            None,
            None,
            "question",
            ""
        )
        suggestions = [
            Suggestion(
                "link",
                "someLink"
            ),
            Suggestion(
                "link",
                "someOtherLink"
            )
        ]
        self.assertFalse(analyse_link_or_question_without_request_data(request, suggestions))
