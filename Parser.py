import json


class Parser:
    def __init__(self, path):
        self.path = path
        with open(path, 'r') as data:
            self.data = json.loads(str(data.read()))

    def get_name(self):
        return self.data["name"]

    def get_dt(self):
        return self.data["dt"]

    def get_Fmax(self):
        return self.data["Fmax"]

    def get_circles(self):
        return self.data["circles"]
