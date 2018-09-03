CHATKEY_IDENTIFIER = 'chatkey'
QUERY_IDENTIFIER = 'query'
MESSAGE_TYPE_IDENTIFIER = 'type'
PERSON_TO_JSON_CODE = {
    'asker': 0,
    'agent': 1
}


def _get_json_for_version10(request, chat_key):
    return {
        CHATKEY_IDENTIFIER: chat_key,
        QUERY_IDENTIFIER: request.get_message(),
        MESSAGE_TYPE_IDENTIFIER: PERSON_TO_JSON_CODE[request.get_person()]
    }


def _get_json_for_version11(request, chat_key):
    return _get_json_for_version10(request, chat_key)


_WHISPER_API_VERSION_TO_GET_JSON_FUNCTION = {
    '10': _get_json_for_version10,
    '11': _get_json_for_version11
}


def get_json(whisper_api_version, request, chat_key):
    return _WHISPER_API_VERSION_TO_GET_JSON_FUNCTION[whisper_api_version](request, chat_key)
