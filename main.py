class Company:
    def __init__(self, name, location, resources, quantity, time):
        self.name = name
        self.location = location
        self.resources = []
        for i in range(len(resources)):
            self.resources.append((resources[i], quantity[i]))
        self.time = time

class Organization:
    def __init__(self, name, location, resources, quantity, time):
        self.name = name
        self.location = location
        self.resources = []
        for i in range(len(resources)):
            self.resources.append((resources[i], quantity[i]))
        self.time = time

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
    if type == "Company":
        name = input("What is your company called?")
        location = input("What is your company's address?")
        resource = [input("What resource can you provide?")]
        quantity = [input("How many can you provide?")]
        time = [int(input("In how many days can you deliver this item (type a number)?"))]
        return Company(name, location, resource, quantity, time)
    else:
        name = input("What is your organization called?")
        location = input("What is your organization's address?")
        resource = [input("What resource do you need?")]
        quantity = [int(input("How many do you need?"))]
        time = [int(input("In how many days do you need it by (type a number)?"))]
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
