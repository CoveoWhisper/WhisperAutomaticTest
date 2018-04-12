TARGET_RESPONSE_TIME_SECONDS = 3.0


class QualityIndexesAnalyzer:
    _metrics_analyzer = None

    def __init__(self, metrics_analyzer):
        self._metrics_analyzer = metrics_analyzer

    def get_pertinence_index(self):
        return (
                self._metrics_analyzer.calculate_number_of_selected_suggestions() /
                self._metrics_analyzer.calculate_total_number_of_suggestions_updates()
        )

    def get_precision_index(self):
        return (
                self._metrics_analyzer.calculate_number_of_selected_suggestions() -
                self._metrics_analyzer.calculate_number_of_modified_suggestions()
        ) / self._metrics_analyzer.calculate_number_of_selected_suggestions()

    def get_clarity_index(self):
        return (
            self._metrics_analyzer.calculate_number_of_selected_suggestions() -
            self._metrics_analyzer.calculate_number_of_opened_suggestions()
        ) / self._metrics_analyzer.calculate_number_of_selected_suggestions()

    def get_speed_index(self):
        return (
                       TARGET_RESPONSE_TIME_SECONDS -
                       self._metrics_analyzer.calculate_average_system_response_time()
        ) / TARGET_RESPONSE_TIME_SECONDS

    def get_relative_confidence_level_accuracy_index(self):
        return 1.0 / self._metrics_analyzer.calculate_mean_position_of_chosen_suggestion()

    def get_intent_accuracy_index(self):
        return (
            self._metrics_analyzer.calculate_total_number_of_suggestions_updates() -
            self._metrics_analyzer.calculate_number_of_unwanted_suggestions_updates()
        ) / self._metrics_analyzer.calculate_total_number_of_suggestions_updates()

    def get_confidence_index(self):
        return self._metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions()
