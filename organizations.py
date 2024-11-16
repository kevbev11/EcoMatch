class Companies:
    def __init__(self, name, location, resources, quantity, time):
        self.name = name
        self.location = location
        self.resources = []
        for i in range(len(resources)):
            self.resources.append((resources[i], quantity[i]))
        self.time = time

class Organizations:
    def __init__(self, name, location, resources, quantity, time):
        self.name = name
        self.location = location
        self.resources = []
        for i in range(len(resources)):
            self.resources.append((resources[i], quantity[i]))
        self.time = time