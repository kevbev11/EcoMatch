class Company:
    def __init__(self, name, location, resources, quantity, time):
        self.name = name
        self.location = location
        self.resources = []
        for i in range(len(resources)):
            self.resources.append((resources[i], quantity[i]))
        self.time = time

    def __repr__(self):
        resources = ''
        for r, q in self.resources:
            resources = resources + f'{q} ' + r + ', '
        resources = resources[:len(resources) - 2]
        return f'{self.name} at {self.location} can provide {resources} in {self.time} days'

class Organization:
    def __init__(self, name, location, resources, quantity, time):
        self.name = name
        self.location = location
        self.resources = []
        for i in range(len(resources)):
            self.resources.append((resources[i], quantity[i]))
        self.time = time

    def __repr__(self):
        resources = ''
        for r, q in self.resources:
            resources = resources + f'{q} ' + r + ', '
        resources = resources[:len(resources) - 2]
        return f'{self.name} at {self.location} needs {resources} in {self.time} days'