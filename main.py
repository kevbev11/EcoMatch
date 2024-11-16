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

#picks between company or charity
def getType():
    options = ["Company", "Charitable Oranization"]
    print("Are you a company or a charitable organization?")

    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    
    while True:
        try:
            answer = int(input("Enter your answer (number): "))
            if 1 <= answer <= 2:
                return options[answer - 1]
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

#returns the object
def getInfo(type):
    addResources = True
    resource = []
    quantity = []
    if type == "Company":
        name = input("What is your company called? ")
        location = input("What is your company's address? ")
        while addResources:
            resource.append(input("What resource can you provide? "))
            while True:
                try:
                    quantity.append(int(input("How many can you provide (type a number)? ")))
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")   
            check = input("Would you like to add another resource? [Y]/[N] ")
            if check == 'N':
                addResources = False
        while True:
            try:
                time = int(input("In how many days can you deliver these items (type a number)? "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        return Company(name, location, resource, quantity, time)
    
    else:
        name = input("What is your organization called? ")
        location = input("What is your organization's address? ")
        while addResources:
            resource.append(input("What resource do you need? "))
            while True:
                try:
                    quantity.append(int(input("How many do you need (type a number)? ")))
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
            check = input("Would you like to add another resource? [Y]/[N] ")
            if check == 'N':
                addResources = False
        while True:
            try:
                time = int(input("In how many days do you need these by (type a number)? "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        return Organization(name, location, resource, quantity, time)

def main():
    companies = set()
    orgs = set()
    type = getType()
    if type == "Company":
        companies.add(getInfo(type))
    else:
        orgs.add(getInfo(type))
    print(companies)
    print(orgs)

main()