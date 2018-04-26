import argparse
import datetime

from whisper_automatic_test.metrics_analyzer import MetricsAnalyzer
from whisper_automatic_test.quality_indexes_analyzer import QualityIndexesAnalyzer
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file
from whisper_automatic_test.scenarios_runner import ScenariosRunner
from whisper_automatic_test.suggestions_responses_analyzer import SuggestionsResponsesAnalyzer
from whisper_automatic_test.utility import get_requests, get_flat_suggestions_responses
from whisper_automatic_test.whisper_api_adapter import get_suggestions_from_whisper_api, get_suggestions_endpoint


def main():
    program_arguments = get_program_arguments()
    scenarios_csv_file_path = program_arguments.scenarios_csv_file_path
    whisper_api_base_url = program_arguments.whisper_api_base_url
    is_verbose = program_arguments.verbose

    scenarios = get_scenarios_from_csv_file(scenarios_csv_file_path)

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
    if is_verbose:
        print_failing_requests_information(suggestions_responses_analyzer, scenarios, suggestions_responses)


def get_program_arguments():
    arguments_parser = argparse.ArgumentParser(description='Whisper automatic test runner.')
    arguments_parser.add_argument(
        '-s', '--scenarios-csv-file-path',
        action='store',
        required=True,
        help='Path to the scenarios CSV file',
        metavar='FILE'
    )
    arguments_parser.add_argument(
        '-w', '--whisper-api-base-url',
        action='store',
        required=True,
        help='Whisper API base URL',
        metavar='URL'
    )
    arguments_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print more information',
    )
    return arguments_parser.parse_args()


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
    pertinence_index = quality_indexes_analyzer.get_pertinence_index()
    speed_index = quality_indexes_analyzer.get_speed_index()
    quality_index_name_and_value_pairs = [
        ('Pertinence index', pertinence_index),
        ('Speed index', speed_index),
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
    simple_quality_index = (
       pertinence_index +
       speed_index
    ) / 2.0

    print('Quality indexes')
    print('=' * 80)
    for quality_index_name_and_value_pair in quality_index_name_and_value_pairs:
        quality_index_name = quality_index_name_and_value_pair[0]
        quality_index_value = quality_index_name_and_value_pair[1]
        print(quality_index_name, ": ", quality_index_value)

    print('Average quality index: ', average_quality_index)
    print('Simple quality index (average of pertinence and speed indexes): ', simple_quality_index)
    print()


def print_failing_requests_information(suggestions_responses_analyzer, scenarios, suggestions_responses):
    failing_requests = get_failing_requests(scenarios, suggestions_responses, suggestions_responses_analyzer)
    failing_requests_information_messages = [
        'Request #{}. Expected: {}. Actual suggestions: {}.'.format(
            failing_request['index'],
            failing_request['expected'],
            failing_request['suggestions']
        )
        for failing_request in failing_requests
    ]
    print('Failing requests')
    print('=' * 80)
    print('\n'.join(failing_requests_information_messages))
    print()


def get_failing_requests(scenarios, suggestions_responses, suggestions_responses_analyzer):
    requests = get_requests(scenarios)
    flat_suggestions_responses = get_flat_suggestions_responses(suggestions_responses)
    requests_analysis = suggestions_responses_analyzer.analyze_scenarios()
    failing_requests = [
        {
            'index': i,
            'expected': '{{success_condition: {}, data: {}}}'.format(
                requests[i].get_success_condition(),
                requests[i].get_data()
            ),
            'suggestions': flat_suggestions_responses[i].get_suggestions()
        }
        for i, request_analysis in enumerate(requests_analysis)
        if request_analysis.startswith('fail')
    ]
    return failing_requests


if __name__ == "__main__":
    main()
