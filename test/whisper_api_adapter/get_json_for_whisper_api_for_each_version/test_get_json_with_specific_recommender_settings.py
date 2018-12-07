import unittest

from whisper_automatic_test.request import Request
from whisper_automatic_test.whisper_api_adapter.json_for_whisper_api import get_overriden_recommender_settings
from whisper_automatic_test.whisper_api_adapter.recommenders import RecommenderType
from whisper_automatic_test.whisper_api_adapter.whisper_api_adapter import get_json_for_whisper_api


class TestGetJsonWithSpecificRecommenderSettings(unittest.TestCase):
    def test_get_overriden_recommender_settings(self):
        expected_settings = {
            'useLongQuerySearchRecommender': False,
            'usePreprocessedQuerySearchRecommender': False,
            'useAnalyticsSearchRecommender': True,
            'useFacetQuestionRecommender': True
        }
        actual_settings = get_overriden_recommender_settings(
            [RecommenderType.AnalyticsSearch, RecommenderType.FacetQuestion]
        )
        self.assertEquals(expected_settings, actual_settings)

    def test_with_recommender_settings(self):
        request = Request('asker', 'Hello world', 'To ignore', 'To ignore')
        used_recommenders = [RecommenderType.AnalyticsSearch, RecommenderType.FacetQuestion]
        actual_json = get_json_for_whisper_api('14', request, 'myChatKey', used_recommenders)
        expected_json = {
            'chatkey': 'myChatKey',
            'query': 'Hello world',
            'type': 0,
            'maxDocuments': 15,
            'maxQuestions': 15,
            'overridenRecommenderSettings': {
                'useLongQuerySearchRecommender': False,
                'usePreprocessedQuerySearchRecommender': False,
                'useAnalyticsSearchRecommender': True,
                'useFacetQuestionRecommender': True
            }
        }
        self.assertEquals(expected_json, actual_json)
