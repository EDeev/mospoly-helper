import json


class JsonTools:
    def __init__(self, user_id):
        self.f_name = f"../data/users/{user_id}.json"

    def save_json(self, data):
        with open(self.f_name, "w", encoding="utf8") as f:
            return json.dump(data, f)

    def read_json(self):
        with open(self.f_name, "r", encoding="utf8") as f:
            return json.load(f)

    def get_buildings(self):
        return self.read_json().keys()