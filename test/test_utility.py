import unittest
from unittest.mock import sentinel

from whisper_automatic_test.utility import get_flat_suggestions_responses


class TestUtility(unittest.TestCase):
    def test_get_flat_suggestions_responses(self):
        suggestions_responses_for_each_scenario = [
            [
                sentinel.a
            ],
            [
                sentinel.b,
                sentinel.c
            ],
            [
                sentinel.d,
                sentinel.e,
                sentinel.f
            ]
        ]
        flat_suggestions_responses = get_flat_suggestions_responses(suggestions_responses_for_each_scenario)
        self.assertEquals(6, len(flat_suggestions_responses))
        self.assertEquals(sentinel.a, flat_suggestions_responses[0])
        self.assertEquals(sentinel.b, flat_suggestions_responses[1])
        self.assertEquals(sentinel.c, flat_suggestions_responses[2])
        self.assertEquals(sentinel.d, flat_suggestions_responses[3])
        self.assertEquals(sentinel.e, flat_suggestions_responses[4])
        self.assertEquals(sentinel.f, flat_suggestions_responses[5])
