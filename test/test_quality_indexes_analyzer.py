import unittest
from datetime import timedelta
from unittest.mock import Mock

from whisper_automatic_test.quality_indexes_analyzer import QualityIndexesAnalyzer


class TestQualityIndexesAnalyzer(unittest.TestCase):
    def setUp(self):
        self._quality_indexes_analyzer = _get_quality_indexes_analyzer_with_different_values_for_each_metric()

    def test_pertinence_index(self):
        self.assertAlmostEquals(-15, self._quality_indexes_analyzer.get_pertinence_index(), places=3)

    def test_pertinence_index_with_zero_wanted_updates(self):
        self.assertAlmostEquals(
            float("-inf"),
            _get_quality_indexes_analyzer_with_zero_wanted_updates().get_pertinence_index(),
            places=3
        )

    def test_speed_index(self):
        self.assertAlmostEquals(-2.333, self._quality_indexes_analyzer.get_speed_index(), places=3)

    def test_relative_confidence_level_accuracy_index(self):
        self.assertAlmostEquals(0.083, self._quality_indexes_analyzer.get_relative_confidence_level_accuracy_index(),
                                places=3)

    def test_intent_accuracy_index(self):
        self.assertAlmostEquals(-0.077, self._quality_indexes_analyzer.get_intent_accuracy_index(), places=3)

    def test_intent_accuracy_index_with_zero_suggestions_updates(self):
        self.assertAlmostEquals(
            1,
            _get_quality_indexes_analyzer_with_zero_suggestions_updates().get_intent_accuracy_index(),
            places=3
        )

    def test_confidence_index(self):
        self.assertAlmostEquals(20.000, self._quality_indexes_analyzer.get_confidence_index(), places=3)


def _get_quality_indexes_analyzer_with_different_values_for_each_metric():
    mock_metrics_analyzer = Mock()
    quality_indexes_analyzer = QualityIndexesAnalyzer(mock_metrics_analyzer)
    mock_metrics_analyzer.calculate_average_system_response_time.return_value = timedelta(seconds=10)
    mock_metrics_analyzer.calculate_messages_number.return_value = 11
    mock_metrics_analyzer.calculate_mean_position_of_selected_suggestions.return_value = 12
    mock_metrics_analyzer.calculate_total_number_of_suggestions_updates.return_value = 13
    mock_metrics_analyzer.calculate_number_of_unwanted_suggestions_updates.return_value = 14
    mock_metrics_analyzer.calculate_number_of_selected_suggestions.return_value = 15
    mock_metrics_analyzer.calculate_number_of_suggested_questions.return_value = 18
    mock_metrics_analyzer.calculate_number_of_suggested_links.return_value = 19
    mock_metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions.return_value = 20
    return quality_indexes_analyzer


def _get_quality_indexes_analyzer_with_zero_wanted_updates():
    mock_metrics_analyzer = Mock()
    quality_indexes_analyzer = QualityIndexesAnalyzer(mock_metrics_analyzer)
    mock_metrics_analyzer.calculate_average_system_response_time.return_value = timedelta(seconds=10)
    mock_metrics_analyzer.calculate_messages_number.return_value = 11
    mock_metrics_analyzer.calculate_mean_position_of_selected_suggestions.return_value = 12
    mock_metrics_analyzer.calculate_total_number_of_suggestions_updates.return_value = 666
    mock_metrics_analyzer.calculate_number_of_unwanted_suggestions_updates.return_value = 666
    mock_metrics_analyzer.calculate_number_of_selected_suggestions.return_value = 15
    mock_metrics_analyzer.calculate_number_of_suggested_questions.return_value = 18
    mock_metrics_analyzer.calculate_number_of_suggested_links.return_value = 19
    mock_metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions.return_value = 20
    return quality_indexes_analyzer


def _get_quality_indexes_analyzer_with_zero_suggestions_updates():
    mock_metrics_analyzer = Mock()
    quality_indexes_analyzer = QualityIndexesAnalyzer(mock_metrics_analyzer)
    mock_metrics_analyzer.calculate_average_system_response_time.return_value = timedelta(seconds=10)
    mock_metrics_analyzer.calculate_messages_number.return_value = 11
    mock_metrics_analyzer.calculate_mean_position_of_selected_suggestions.return_value = 12
    mock_metrics_analyzer.calculate_total_number_of_suggestions_updates.return_value = 0
    mock_metrics_analyzer.calculate_number_of_unwanted_suggestions_updates.return_value = 14
    mock_metrics_analyzer.calculate_number_of_selected_suggestions.return_value = 15
    mock_metrics_analyzer.calculate_number_of_suggested_questions.return_value = 18
    mock_metrics_analyzer.calculate_number_of_suggested_links.return_value = 19
    mock_metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions.return_value = 20
    return quality_indexes_analyzer
