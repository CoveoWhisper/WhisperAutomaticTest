import unittest
from unittest.mock import Mock

from whisper_automatic_test.quality_indexes_analyzer import QualityIndexesAnalyzer


class TestQualityIndexesAnalyzer(unittest.TestCase):
    _mock_metrics_analyzer = None
    _quality_indexes_analyzer = None

    def setUp(self):
        self._mock_metrics_analyzer = Mock()
        self._quality_indexes_analyzer = QualityIndexesAnalyzer(self._mock_metrics_analyzer)

        self._mock_metrics_analyzer.calculate_average_system_response_time.return_value = 10
        self._mock_metrics_analyzer.calculate_messages_number.return_value = 11
        self._mock_metrics_analyzer.calculate_mean_position_of_chosen_suggestion.return_value = 12
        self._mock_metrics_analyzer.calculate_total_number_of_suggestions_updates.return_value = 13
        self._mock_metrics_analyzer.calculate_number_of_unwanted_suggestions_updates.return_value = 14
        self._mock_metrics_analyzer.calculate_number_of_selected_suggestions.return_value = 15
        self._mock_metrics_analyzer.calculate_number_of_suggested_questions.return_value = 18
        self._mock_metrics_analyzer.calculate_number_of_suggested_links.return_value = 19
        self._mock_metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions.return_value = 20

    def test_pertinence_index(self):
        self.assertAlmostEquals(1.154, self._quality_indexes_analyzer.get_pertinence_index(), places=3)

    def test_speed_index(self):
        self.assertAlmostEquals(-2.333, self._quality_indexes_analyzer.get_speed_index(), places=3)

    def test_relative_confidence_level_accuracy_index(self):
        self.assertAlmostEquals(0.083, self._quality_indexes_analyzer.get_relative_confidence_level_accuracy_index(),
                                places=3)

    def test_intent_accuracy_index(self):
        self.assertAlmostEquals(-0.077, self._quality_indexes_analyzer.get_intent_accuracy_index(), places=3)

    def test_confidence_index(self):
        self.assertAlmostEquals(20.000, self._quality_indexes_analyzer.get_confidence_index(), places=3)
