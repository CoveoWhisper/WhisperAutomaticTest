CHATKEY_IDENTIFIER = 'chatkey'
QUERY_IDENTIFIER = 'query'
QUERY_IDENTIFIER_LEGACY_TYPO = 'querry'  # Required for retrocompatibility with previous API contract
MESSAGE_TYPE_IDENTIFIER = 'type'
PERSON_TO_JSON_CODE = {
    'asker': 0,
    'agent': 1
}


def get_json_for_version10(request, chat_key):
    return {
        CHATKEY_IDENTIFIER: chat_key,
        QUERY_IDENTIFIER: request.get_message(),
        QUERY_IDENTIFIER_LEGACY_TYPO: request.get_message(),
        MESSAGE_TYPE_IDENTIFIER: PERSON_TO_JSON_CODE[request.get_person()]
    }


WHISPER_API_VERSION_TO_GET_JSON_FUNCTION = {
    '10': get_json_for_version10
}
