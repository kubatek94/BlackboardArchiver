import requests

class Blackboard(requests.Session):
    def __init__(self):
        super(Blackboard, self).__init__()

    def set_user(self, user):
        self.user = user

    def set_school(self, school):
        self.school = school