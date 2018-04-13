import json
import requests

from whisper_automatic_test.suggestion import Suggestion

URL = 'https://whisper.us-east-1.elasticbeanstalk.com/whisper/suggestions'
CHAT_KEY_IDENTIFIER = 'chatkey'
QUERY_IDENTIFIER = 'querry'


def get_json_for_whisper_api(request, chat_key):
    return {
        CHAT_KEY_IDENTIFIER: chat_key,
        QUERY_IDENTIFIER: request.get_message(),
    }


def get_suggestions_from_whisper_api(request, chat_key):
    whisper_response = requests.post(URL, json=get_json_for_whisper_api(request, chat_key)).content.decode("utf-8")
    return whisper_response_to_suggestions(whisper_response)


def whisper_response_to_suggestions(whisper_response):
    def get_suggestion(json_suggestion):
        is_link = 'printableUri' in json_suggestion
        suggestion_type = 'link' if is_link else 'question'
        data_json_field = 'printableUri' if is_link else 'title'
        return Suggestion(suggestion_type, json_suggestion[data_json_field])

    json_response = json.loads(whisper_response)
    return [get_suggestion(json_suggestion) for json_suggestion in json_response]



