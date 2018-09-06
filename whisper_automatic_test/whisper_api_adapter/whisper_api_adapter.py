import json
import requests

from whisper_automatic_test.suggestion import Suggestion
from whisper_automatic_test.whisper_api_adapter.json_for_whisper_api import get_json

SUGGESTIONS_ENDPOINT_SUFFIX = 'whisper/suggestions'
VERSION_ENDPOINT_SUFFIX = 'whisper/version'


def get_whisper_api_version(whisper_api_base_url):
    whisper_response = requests.get(
        get_version_endpoint(whisper_api_base_url)
    )
    json_response = json.loads(whisper_response.content.decode('utf8'))
    return json_response['version']


def get_json_for_whisper_api(whisper_api_version, request, chat_key):
    return get_json(whisper_api_version, request, chat_key)


def get_suggestions_from_whisper_api(whisper_api_version, whisper_api_suggestions_endpoint, request, chatkey):
    request_payload = get_json_for_whisper_api(whisper_api_version, request, chatkey)
    whisper_response = requests.post(
        whisper_api_suggestions_endpoint,
        json=request_payload
    )
    return whisper_response_to_suggestions(whisper_api_version, whisper_response.content.decode("utf-8"))


def _whisper_response_to_suggestions_version10(whisper_response):
    def get_suggestion(json_suggestion):
        is_link = 'printableUri' in json_suggestion
        suggestion_type = 'link' if is_link else 'question'
        data_json_field = 'printableUri' if is_link else 'title'
        return Suggestion(suggestion_type, json_suggestion[data_json_field])

    json_response = json.loads(whisper_response)
    return [get_suggestion(json_suggestion) for json_suggestion in json_response]


def _whisper_response_to_suggestions_version11(whisper_response):
    def json_question_to_suggestion(json_question):
        return Suggestion('question', json_question['title'])

    def json_link_to_suggestion(json_link):
        return Suggestion('link', json_link['printableUri'])

    json_response = json.loads(whisper_response)
    json_questions = json_response['questions']
    if json_questions:
        questions = [json_question_to_suggestion(json_question) for json_question in json_questions]
    else:
        questions = []
    json_links = json_response['suggestedDocuments']
    if json_links:
        links = [json_link_to_suggestion(json_link) for json_link in json_links]
    else:
        links = []
    return links + questions


_WHISPER_RESPONSE_TO_SUGGESTIONS_BY_API_VERSION_FUNCTION = {
    '10': _whisper_response_to_suggestions_version10,
    '11': _whisper_response_to_suggestions_version11
}


def whisper_response_to_suggestions(whisper_api_version, whisper_response):
    return _WHISPER_RESPONSE_TO_SUGGESTIONS_BY_API_VERSION_FUNCTION[whisper_api_version](whisper_response)


def _get_endpoint(base_url, endpoint_suffix):
    suggestions_endpoint = base_url
    suggestions_endpoint += '' if base_url.endswith('/') else '/'
    suggestions_endpoint += endpoint_suffix
    return suggestions_endpoint


def get_suggestions_endpoint(base_url):
    return _get_endpoint(base_url, SUGGESTIONS_ENDPOINT_SUFFIX)


def get_version_endpoint(base_url):
    return _get_endpoint(base_url, VERSION_ENDPOINT_SUFFIX)
