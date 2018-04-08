import csv
from whisper_automatic_test.scenario import Scenario
from whisper_automatic_test.request import Request


def get_scenarios_from_csv_file(scenario_csv_file_path):
    scenarios = []
    with open(scenario_csv_file_path, newline='') as csv_file:
        scenario_reader = csv.reader(csv_file, delimiter=',')
        next(scenario_reader)
        current_scenario_id = None
        current_requests = []
        for row in scenario_reader:
            if row[0] != current_scenario_id:
                update_scenarios(scenarios, current_requests)
                current_scenario_id = row[0]
                current_requests = []
            request = Request(row[1], row[2], row[3], row[4])
            current_requests.append(request)
        update_scenarios(scenarios, current_requests)
    return scenarios


def update_scenarios(scenarios, requests):
    if not requests:
        return

    scenario = Scenario(requests)
    scenarios.append(scenario)
