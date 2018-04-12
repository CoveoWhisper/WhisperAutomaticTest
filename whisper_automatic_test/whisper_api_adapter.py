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
    json_response = json.loads(whisper_response)
    return [Suggestion('link', suggestion['printableUri']) if 'printableUri' in suggestion else Suggestion('question', suggestion['title']) for suggestion in json_response]
