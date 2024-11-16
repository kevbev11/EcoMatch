import users
import distance
# import mostcompatible

#picks between company or charity
def getType():
    options = ["Company", "Charitable Organization", "None"]
    print("Are you a company or a charitable organization?")

    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    
    while True:
        try:
            answer = int(input("Enter your answer (number): "))
            if 1 <= answer <= 3:
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
            quantity.append(getIntValue("How many can you provide? ")) 
            while True:
                check = input("Would you like to add another resource? [Y]/[N] ")
                if check in {'n', 'N'}:
                    addResources = False
                    break
                elif check in {'y', 'Y'}:
                    break
                else:
                    print("Invalid input")
        time = getIntValue("In how many days can you deliver these items? ")
        return users.Company(name, location, resource, quantity, time)
    
    else:
        name = input("What is your organization called? ")
        location = input("What is your organization's address? ")
        while addResources:
            resource.append(input("What resource do you need? "))
            quantity.append(getIntValue("How many do you need? "))
            while True:
                check = input("Would you like to add another resource? [Y]/[N] ")
                if check in {'n', 'N'}:
                    addResources = False
                    break
                elif check in {'y', 'Y'}:
                    break
                else:
                    print("Invalid input")
        time = getIntValue("In how many days do you need these by? ")
        return users.Organization(name, location, resource, quantity, time)

def getIntValue(question):
    while True:
        try:
            value = int(input(question))
            if value < 1:
                print("Invalid input. Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.") 
    return value

def main():
    companies = set()
    orgs = set()
    while True:
        type = getType()
        if type == "Company":
            companies.add(getInfo(type))
        elif type == "Charitable Organization":
            orgs.add(getInfo(type))
        else:
            break
    print(companies)
    print(orgs)

main()