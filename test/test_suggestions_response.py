import unittest
from datetime import timedelta

from whisper_automatic_test.suggestion import Suggestion
from whisper_automatic_test.suggestions_response import SuggestionsResponse


class TestSuggestionsResponse(unittest.TestCase):
    def test_getters(self):
        suggestions = [
            Suggestion('link', 'some_url'),
            Suggestion('link', 'another_url')
        ]
        suggestions_response = SuggestionsResponse(suggestions, timedelta(seconds=42))
        self.assertEquals('link', suggestions_response.get_suggestions()[0].get_type())
        self.assertEquals('some_url', suggestions_response.get_suggestions()[0].get_data())
        self.assertEquals('link', suggestions_response.get_suggestions()[1].get_type())
        self.assertEquals('another_url', suggestions_response.get_suggestions()[1].get_data())
        self.assertEquals(timedelta(seconds=42), suggestions_response.get_response_time_duration())

