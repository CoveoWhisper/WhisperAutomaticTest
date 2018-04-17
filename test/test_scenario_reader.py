import unittest
from whisper_automatic_test.scenario_reader import get_scenarios_from_csv_file

SCENARIO_FILE_PATH = 'test/resources/test_scenarios_for_scenario_reader.csv'


class TestScenarioReader(unittest.TestCase):

    def test_read_scenarios_from_csv_file(self):
        scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        self.assertEquals(2, len(scenarios))

    def test_scenario_with_single_request(self):
        scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        scenario = scenarios[0]
        requests = scenario.get_requests()
        request = requests[0]
        self.assertEquals('asker', request.get_person())
        self.assertEquals('Help, I have problems calling the rest API', request.get_message())
        self.assertEquals('link', request.get_success_condition())
        data = request.get_data()
        self.assertEquals(2, len(data))
        self.assertEquals('https://blog.coveo.com/goodbye-gsa-hello-intelligent-search-in-the-cloud/', data[0])
        self.assertEquals('https://second_url.com/second_url', data[1])

    def test_scenario_with_multiple_requests(self):
        scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        scenario = scenarios[1]
        self.assertEquals(5, len(scenario.get_requests()))
        requests = scenario.get_requests()
        request_a = requests[0]
        request_b = requests[1]

        self.assertEquals('asker', request_a.get_person())
        self.assertEquals('Hello', request_a.get_message())
        self.assertEquals('question', request_a.get_success_condition())
        self.assertEquals('did you try this?', request_a.get_data()[0])

        self.assertEquals('agent', request_b.get_person())
        self.assertEquals('I love potatoes', request_b.get_message())
        self.assertEquals('same', request_b.get_success_condition())
        data = request_b.get_data()
        self.assertEquals(0, len(data))

    def test_notlink_with_multiple_links(self):
        scenarios = get_scenarios_from_csv_file(SCENARIO_FILE_PATH)
        scenario = scenarios[1]
        self.assertEquals(5, len(scenario.get_requests()))
        request_notlink = scenario.get_requests()[3]
        self.assertEquals('asker', request_notlink.get_person())
        self.assertEquals('I love tomatoes', request_notlink.get_message())
        self.assertEquals('notlink', request_notlink.get_success_condition())
        self.assertEquals('https://some_forbidden_website.com', request_notlink.get_data()[0])
        self.assertEquals('https://banned_forum.net', request_notlink.get_data()[1])
