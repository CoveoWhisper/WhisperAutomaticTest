import json
import requests

from whisper_automatic_test.suggestion import Suggestion
from whisper_automatic_test.whisper_api_adapter.json_for_whisper_api import WHISPER_API_VERSION_TO_GET_JSON_FUNCTION

SUGGESTIONS_ENDPOINT_SUFFIX = 'whisper/suggestions'


def get_json_for_whisper_api(whisper_api_version, request, chat_key):
    get_json = WHISPER_API_VERSION_TO_GET_JSON_FUNCTION[whisper_api_version]
    return get_json(request, chat_key)


def get_suggestions_from_whisper_api(whisper_api_version, whisper_api_suggestions_endpoint, request, chatkey):
    whisper_response = requests.post(
        whisper_api_suggestions_endpoint,
        json=get_json_for_whisper_api(whisper_api_version, request, chatkey)
    )
    return whisper_response_to_suggestions(whisper_response.content.decode("utf-8"))


def whisper_response_to_suggestions(whisper_response):
    def get_suggestion(json_suggestion):
        is_link = 'printableUri' in json_suggestion
        suggestion_type = 'link' if is_link else 'question'
        data_json_field = 'printableUri' if is_link else 'title'
        return Suggestion(suggestion_type, json_suggestion[data_json_field])

    json_response = json.loads(whisper_response)
    return [get_suggestion(json_suggestion) for json_suggestion in json_response]


def get_suggestions_endpoint(base_url):
    suggestions_endpoint = base_url
    suggestions_endpoint += '' if base_url.endswith('/') else '/'
    suggestions_endpoint += SUGGESTIONS_ENDPOINT_SUFFIX
    return suggestions_endpoint
