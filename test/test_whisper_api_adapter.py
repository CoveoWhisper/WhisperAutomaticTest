import unittest
from whisper_automatic_test.whisper_api_adapter import get_json_for_whisper_api
from whisper_automatic_test.whisper_api_adapter import whisper_response_to_suggestions
from whisper_automatic_test.request import Request

EXAMPLE_WHISPER_RESPONSE_FILE_PATH = 'test/resources/example_whisper_response_3_links.json'


class TestWhisperApiAdapter(unittest.TestCase):
    def test_request_to_data(self):
        request = Request('asker', 'Hello world', 'To ignore', 'To ignore')
        actual_json = get_json_for_whisper_api(request, 'myChatKey')
        expected_json = {
            'chatkey': 'myChatKey',
            'querry': 'Hello world',
        }
        self.assertEquals(expected_json, actual_json)

    def test_convert_whisper_response_to_suggestions(self):
        with open(EXAMPLE_WHISPER_RESPONSE_FILE_PATH) as file:
            example_whisper_response = file.read()
        suggestions = whisper_response_to_suggestions(example_whisper_response)
        self.assertEquals(3, len(suggestions))
        for suggestion in suggestions:
            self.assertEquals('link', suggestion.get_type())
        self.assertEquals(
            'https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/',
            suggestions[0].get_data()
        )
        self.assertEquals(
            'https://coveo.github.io/search-ui/interfaces/isearchendpointoptions.html',
            suggestions[1].get_data()
        )
        self.assertEquals(
            'https://onlinehelp.coveo.com/en/ces/7.0/Administrator/About_NET_Conversion_Scripts.htm',
            suggestions[2].get_data()
        )
