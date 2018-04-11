class Scenario:
    _requests = None

    def __init__(self, requests):
        self._requests = requests

    def get_requests(self):
        return self._requests
