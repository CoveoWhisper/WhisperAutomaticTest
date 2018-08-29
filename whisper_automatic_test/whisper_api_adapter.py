import json
import requests

from whisper_automatic_test.suggestion import Suggestion

CHATKEY_IDENTIFIER = 'chatkey'
QUERY_IDENTIFIER = 'query'
QUERY_IDENTIFIER_LEGACY_TYPO = 'querry'  # Required for retrocompatibility with previous API contract
MESSAGE_TYPE_IDENTIFIER = 'type'
PERSON_TO_JSON_CODE = {
    'asker': 0,
    'agent': 1
}
SUGGESTIONS_ENDPOINT_SUFFIX = 'whisper/suggestions'


def get_json_for_whisper_api(request, chat_key):
    return {
        CHATKEY_IDENTIFIER: chat_key,
        QUERY_IDENTIFIER: request.get_message(),
        QUERY_IDENTIFIER_LEGACY_TYPO: request.get_message(),
        MESSAGE_TYPE_IDENTIFIER: PERSON_TO_JSON_CODE[request.get_person()]
    }


def get_suggestions_from_whisper_api(whisper_api_suggestions_endpoint, request, chatkey):
    whisper_response = requests.post(
        whisper_api_suggestions_endpoint,
        json=get_json_for_whisper_api(request, chatkey)
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
