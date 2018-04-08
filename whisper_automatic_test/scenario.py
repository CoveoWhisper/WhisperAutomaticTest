class Scenario:
    requests = None

    def __init__(self, requests):
        self.requests = requests

    def get_requests(self):
        return self.requests
