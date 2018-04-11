import unittest

from whisper_automatic_test.suggestion import Suggestion
from whisper_automatic_test.suggestions_response import SuggestionsResponse


class TestSuggestionsResponse(unittest.TestCase):
    def test_getters(self):
        suggestions = [
            Suggestion('link', 'some_url'),
            Suggestion('link', 'another_url')
        ]
        suggestions_response = SuggestionsResponse(suggestions, 42, 90)
        self.assertEquals('link', suggestions_response.get_suggestions()[0].get_type())
        self.assertEquals('some_url', suggestions_response.get_suggestions()[0].get_data())
        self.assertEquals('link', suggestions_response.get_suggestions()[1].get_type())
        self.assertEquals('another_url', suggestions_response.get_suggestions()[1].get_data())
        self.assertEquals(42, suggestions_response.get_timestamp_sent_request())
        self.assertEquals(90, suggestions_response.get_timestamp_received_response())

