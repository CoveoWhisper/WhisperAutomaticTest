from datetime import timedelta

from whisper_automatic_test.exceptions.invalid_timestamp_exception import InvalidTimestampException
from whisper_automatic_test.exceptions.no_requests_exception import NoRequestsException
from whisper_automatic_test.exceptions.no_suggestions_responses_exception import NoSuggestionsResponsesException
from whisper_automatic_test.exceptions.no_suggestions_responses_for_every_requests_exception import \
    NoSuggestionsResponsesForEveryRequestsException


def raise_if_there_is_no_request_in_scenarios(scenarios):
    if not get_requests(scenarios):
        raise NoRequestsException('No requests')


def raise_if_there_is_no_suggestions_responses(suggestions_responses_for_each_scenario):
    if not suggestions_responses_for_each_scenario:
        raise NoSuggestionsResponsesException('No suggestions responses to analyze')


def raise_if_there_is_not_a_suggestions_response_for_every_request(scenarios, suggestions_responses_for_each_scenario):
    no_suggestions_responses_for_every_request_exception = NoSuggestionsResponsesForEveryRequestsException(
        'There is not a suggestions response for every request')
    if len(scenarios) != len(suggestions_responses_for_each_scenario):
        raise no_suggestions_responses_for_every_request_exception
    for i, scenario in enumerate(scenarios):
        suggestions_responses_for_scenario = suggestions_responses_for_each_scenario[i]
        if len(scenario.get_requests()) != len(suggestions_responses_for_scenario):
            raise no_suggestions_responses_for_every_request_exception


def raise_if_there_is_an_invalid_timestamp(suggestions_responses_for_each_scenario):
    for suggestions_responses_for_a_scenario in suggestions_responses_for_each_scenario:
        for suggestion_response in suggestions_responses_for_a_scenario:
            is_valid_timestamp = suggestion_response.get_response_time_duration() >= timedelta(seconds=0)
            if not is_valid_timestamp:
                raise InvalidTimestampException(
                    'Received timestamp of response should not be smaller than sent timestamp')


def get_requests(scenarios):
    requests = []
    for scenario in scenarios:
        requests += scenario.get_requests()
    return requests


def get_flat_suggestions_responses(suggestions_responses):
    return sum(suggestions_responses, [])
