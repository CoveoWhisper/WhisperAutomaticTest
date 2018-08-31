import unittest

from whisper_automatic_test.whisper_api_adapter.whisper_api_adapter import get_suggestions_endpoint


class TestGetSuggestionsEndpoint(unittest.TestCase):
    def test_get_suggestions_endpoint(self):
        self.assertEquals(
            'potato.com/whisper/suggestions',
            get_suggestions_endpoint('potato.com')
        )

    def test_get_suggestions_endpoint_with_base_url_already_ending_with_slash(self):
        self.assertEquals(
            'potato.com/whisper/suggestions',
            get_suggestions_endpoint('potato.com/')
        )
