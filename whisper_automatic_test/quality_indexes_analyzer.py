from datetime import timedelta

TARGET_RESPONSE_TIME_SECONDS = timedelta(seconds=3)


class QualityIndexesAnalyzer:
    _metrics_analyzer = None

    def __init__(self, metrics_analyzer):
        self._metrics_analyzer = metrics_analyzer

    def get_pertinence_index(self):
        number_of_wanted_suggestions_updates = (
            self._metrics_analyzer.calculate_total_number_of_suggestions_updates() -
            self._metrics_analyzer.calculate_number_of_unwanted_suggestions_updates()
        )
        if 0 == number_of_wanted_suggestions_updates:
            return float('-inf')
        return (
                self._metrics_analyzer.calculate_number_of_selected_suggestions() /
                number_of_wanted_suggestions_updates
        )

    def get_speed_index(self):
        return (
                       TARGET_RESPONSE_TIME_SECONDS -
                       self._metrics_analyzer.calculate_average_system_response_time()
        ) / TARGET_RESPONSE_TIME_SECONDS

    def get_relative_confidence_level_accuracy_index(self):
        return 1.0 / self._metrics_analyzer.calculate_mean_position_of_selected_suggestions()

    def get_intent_accuracy_index(self):
        return (
            self._metrics_analyzer.calculate_total_number_of_suggestions_updates() -
            self._metrics_analyzer.calculate_number_of_unwanted_suggestions_updates()
        ) / self._metrics_analyzer.calculate_total_number_of_suggestions_updates()

    def get_confidence_index(self):
        return self._metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions()
