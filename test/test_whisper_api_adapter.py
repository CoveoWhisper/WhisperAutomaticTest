import unittest
from whisper_automatic_test.whisper_api_adapter import get_json_for_whisper_api
from whisper_automatic_test.request import Request


class TestWhisperApiAdapter(unittest.TestCase):

    def test_request_to_data(self):
        request = Request('asker', 'Hello world', 'To ignore', 'To ignore')
        actual_json = get_json_for_whisper_api(request, 'myChatKey')
        expected_json = {
            'chatkey': 'myChatKey',
            'querry': 'Hello world',
        }
        self.assertEquals(expected_json, actual_json)
