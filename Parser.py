import json
from recordclass import recordclass


class Parser:
    def __init__(self, path):
        self.path = path
        with open(path, 'r') as data:
            self.data = json.loads(data.read(), object_hook=lambda d: recordclass('Environment', d.keys())(*d.values()))

    @property
    def name(self):
        return self.data.name

    @property
    def dt(self):
        return self.data.dt

    @property
    def fmax(self):
        return self.data.Fmax

    @property
    def circles(self):
        return self.data.circles
