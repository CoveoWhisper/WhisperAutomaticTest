import datetime
import sys

from whisper_automatic_test.metrics_analyzer import MetricsAnalyzer
from whisper_automatic_test.quality_indexes_analyzer import QualityIndexesAnalyzer
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file
from whisper_automatic_test.scenarios_runner import ScenariosRunner
from whisper_automatic_test.suggestions_responses_analyzer import SuggestionsResponsesAnalyzer
from whisper_automatic_test.whisper_api_adapter import get_suggestions_from_whisper_api, get_suggestions_endpoint


def main():
    arguments = sys.argv
    assert 2 <= len(arguments) and 'Missing argument: scenario CSV file path.'
    assert 3 == len(arguments) and 'Missing argument: Whisper API URL.'
    csv_scenarios_file_path = arguments[1]
    whisper_api_base_url = arguments[2]

    scenarios = get_scenarios_from_csv_file(csv_scenarios_file_path)

    def get_suggestions(request, chatkey):
        return get_suggestions_from_whisper_api(
            get_suggestions_endpoint(whisper_api_base_url),
            request,
            chatkey)

    scenario_runner = ScenariosRunner(get_suggestions, get_time)
    suggestions_responses = scenario_runner.run(scenarios)
    suggestions_responses_analyzer = SuggestionsResponsesAnalyzer(scenarios, suggestions_responses)
    metrics_analyzer = MetricsAnalyzer(scenarios, suggestions_responses)
    quality_indexes_analyzer = QualityIndexesAnalyzer(metrics_analyzer)

    print_suggestions_responses_analysis(suggestions_responses_analyzer)
    print_metrics(metrics_analyzer)
    print_quality_indexes(quality_indexes_analyzer)

    pass


def get_time():
    return datetime.datetime.utcnow()


def print_suggestions_responses_analysis(suggestions_responses_analyzer):
    print('Scenario results')
    print('=' * 80)
    print(suggestions_responses_analyzer.analyze_to_string())
    print()


def print_metrics(metrics_analyzer):
    metric_name_and_value_pairs = [
        ('Average system response time', metrics_analyzer.calculate_average_system_response_time()),
        ('Total number of messages', metrics_analyzer.calculate_messages_number()),
        ('Mean position of selected suggestions', metrics_analyzer.calculate_mean_position_of_selected_suggestions()),
        ('Total number of suggestions updates', metrics_analyzer.calculate_total_number_of_suggestions_updates()),
        ('Number of unwanted suggestions updates', metrics_analyzer.calculate_number_of_unwanted_suggestions_updates()),
        ('Number of selected suggestions', metrics_analyzer.calculate_number_of_selected_suggestions()),
        ('Number of suggested questions', metrics_analyzer.calculate_number_of_suggested_questions()),
        ('Number of suggested links', metrics_analyzer.calculate_number_of_suggested_links()),
        (
            'Mean confidence level of selected suggestions',
            metrics_analyzer.calculate_mean_confidence_level_of_selected_suggestions()
        )
    ]

    print('Metrics')
    print('=' * 80)
    for metric_name_and_value_pair in metric_name_and_value_pairs:
        metric_name = metric_name_and_value_pair[0]
        metric_value = metric_name_and_value_pair[1]
        print(metric_name, ": ", metric_value)
    print()


def print_quality_indexes(quality_indexes_analyzer):
    quality_index_name_and_value_pairs = [
        ('Pertinence index', quality_indexes_analyzer.get_pertinence_index()),
        ('Speed index', quality_indexes_analyzer.get_speed_index()),
        (
            'Relative confidence level accuracy index',
            quality_indexes_analyzer.get_relative_confidence_level_accuracy_index()),
        ('Intent accuracy index', quality_indexes_analyzer.get_intent_accuracy_index()),
        ('Confidence index', quality_indexes_analyzer.get_confidence_index()),
    ]
    average_quality_index = (
            sum(
                quality_index_name_and_value_pair[1]
                for quality_index_name_and_value_pair in quality_index_name_and_value_pairs
            ) / len(quality_index_name_and_value_pairs)
    )

    print('Quality indexes')
    print('=' * 80)
    for quality_index_name_and_value_pair in quality_index_name_and_value_pairs:
        quality_index_name = quality_index_name_and_value_pair[0]
        quality_index_value = quality_index_name_and_value_pair[1]
        print(quality_index_name, ": ", quality_index_value)

    print('Average quality index: ', average_quality_index)


if __name__ == "__main__":
    main()
