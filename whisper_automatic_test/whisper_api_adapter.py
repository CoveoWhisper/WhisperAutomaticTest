import requests


URL = 'https://whisper.us-east-1.elasticbeanstalk.com/whisper/suggestions'
CHAT_KEY_IDENTIFIER = 'chatkey'
QUERY_IDENTIFIER = 'querry'


def get_json_for_whisper_api(request, chat_key):
    return {
        CHAT_KEY_IDENTIFIER: chat_key,
        QUERY_IDENTIFIER: request.get_message(),
    }


def get_suggestions_from_whisper_api(request, chat_key):
    response = requests.post(URL, json=get_json_for_whisper_api(request, chat_key))
    return response.content.decode("utf-8")
