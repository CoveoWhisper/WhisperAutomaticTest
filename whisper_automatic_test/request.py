class Request:
    person = None
    message = None
    success_condition = None
    data = None

    def __init__(self, person, message, success_condition, raw_data):
        self.person = person
        self.message = message
        self.success_condition = success_condition
        self.data = raw_data.split()

    def get_person(self):
        return self.person

    def get_message(self):
        return self.message

    def get_success_condition(self):
        return self.success_condition

    def get_data(self):
        return self.data
