import unittest
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file

scenario_file_path = 'test/resources/test_scenario.csv'


class TestScenarioReader(unittest.TestCase):

    def test_read_scenarios_from_csv_file(self):
        scenarios = get_scenarios_from_csv_file(scenario_file_path)
        self.assertEquals(2, len(scenarios))

    def test_scenario_with_single_request(self):
        scenarios = get_scenarios_from_csv_file(scenario_file_path)
        scenario = scenarios[0]
        requests = scenario.get_requests()
        request = requests[0]
        self.assertEquals('asker', request.get_person())
        self.assertEquals('I have problems calling the rest API', request.get_message())
        self.assertEquals('link', request.get_success_condition())
        self.assertEquals('https://blablabla.com/blablabla', request.get_data())

    def test_scenario_with_multiple_requests(self):
        scenarios = get_scenarios_from_csv_file(scenario_file_path)
        scenario = scenarios[1]
        self.assertEquals(2, len(scenario.get_requests()))
        requests = scenario.get_requests()
        request_a = requests[0]
        request_b = requests[1]

        self.assertEquals('asker', request_a.get_person())
        self.assertEquals('Hello', request_a.get_message())
        self.assertEquals('same', request_a.get_success_condition())
        self.assertEquals('', request_a.get_data())

        self.assertEquals('agent', request_b.get_person())
        self.assertEquals('World', request_b.get_message())
        self.assertEquals('link', request_b.get_success_condition())
        self.assertEquals('https://asdasd.com/asdasd', request_b.get_data())
