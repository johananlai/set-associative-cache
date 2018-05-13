
class Student:

    def __init__(self, name, sid, study, interests=set()):
        self._name = name
        self._sid = sid
        self._school = study[0]
        self._major = study[1]
        self._interests = interests

    def change_study(self, study):
        self._school = study[0]
        self._major = study[1]

    def add_interest(self, interest):
        self._interests.add(interest)
        return 1

    def get_name(self):
        return self._name

    def get_id(self):
        return self._sid

    def get_study(self):
        return self._school, self._major

    def get_interests(self):
        return self._interests
