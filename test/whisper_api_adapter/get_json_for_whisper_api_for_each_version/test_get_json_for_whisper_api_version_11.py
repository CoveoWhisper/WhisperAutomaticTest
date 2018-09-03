import unittest

from whisper_automatic_test.request import Request
from whisper_automatic_test.whisper_api_adapter.whisper_api_adapter import get_json_for_whisper_api


class TestGetJsonVersion11(unittest.TestCase):
    def test_request_to_data_type_asker(self):
        request = Request('asker', 'Hello world', 'To ignore', 'To ignore')
        actual_json = get_json_for_whisper_api('11', request, 'myChatKey')
        expected_json = {
            'chatkey': 'myChatKey',
            'query': 'Hello world',
            'type': 0
        }
        self.assertEquals(expected_json, actual_json)

    def test_request_to_data_type_agent(self):
        request = Request('agent', 'Hello world', 'To ignore', 'To ignore')
        actual_json = get_json_for_whisper_api('11', request, 'myChatKey')
        expected_json = {
            'chatkey': 'myChatKey',
            'query': 'Hello world',
            'type': 1
        }
        self.assertEquals(expected_json, actual_json)
