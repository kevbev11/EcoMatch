import users
#global sets for companies and orgs here
companies = set()
orgs = set()
currComp = None
currOrg = None

company1 = users.Company(
    name="Green Suppliers Inc.",
    email="contact@greensuppliers.com",
    phone="123-456-7890",
    address="Pittsburgh, PA",
    resources=["lumber", "tarps", "plywood"],
    quantity=[100, 50, 200],
    time=7
)

company2 = users.Company(
    name="TechParts Co.",
    email="support@techparts.com",
    phone="987-654-3210",
    address="Pittsburgh, PA",
    resources=["laptops", "power banks", "charging cables"],
    quantity=[50, 200, 300],
    time=5
)

company3 = users.Company(
    name="Fresh Farms",
    email="info@freshfarms.com",
    phone="111-222-3333",
    address="Pittsburgh, PA",
    resources=["fresh produce", "canned goods", "bottled water"],
    quantity=[500, 1000, 2000],
    time=3
)

company4 = users.Company(
    name="BuildMax",
    email="sales@buildmax.com",
    phone="222-333-4444",
    address="Pittsburgh, PA",
    resources=["bricks", "roofing tiles", "insulation materials"],
    quantity=[1000, 500, 300],
    time=10
)

company5 = users.Company(
    name="Global Chemicals",
    email="support@globalchemicals.com",
    phone="333-444-5555",
    address="Pittsburgh, PA",
    resources=["hand sanitizer", "cleaning supplies", "disinfectant sprays"],
    quantity=[200, 500, 300],
    time=7
)

organization1 = users.Organization(
    name="Housing Initiative",
    email="contact@housinginitiative.org",
    phone="888-999-0000",
    address="Pittsburgh, PA",
    resources=["lumber", "plywood", "tarps"],
    quantity=[50, 20, 100],
    time=10
)

organization2 = users.Organization(
    name="Tech Education Group",
    email="info@teched.org",
    phone="777-888-9999",
    address="Pittsburgh, PA",
    resources=["laptops", "power banks", "charging cables"],
    quantity=[30, 50, 60],
    time=7
)

organization3 = users.Organization(
    name="Food Relief",
    email="support@foodrelief.org",
    phone="666-777-8888",
    address="Pittsburgh, PA",
    resources=["fresh produce", "canned goods", "bottled water"],
    quantity=[200, 150, 300],
    time=5
)

organization4 = users.Organization(
    name="Clean Water Foundation",
    email="contact@cleanwater.org",
    phone="555-666-7777",
    address="Pittsburgh, PA",
    resources=["filters", "bottled water", "water tanks"],
    quantity=[50, 200, 10],
    time=14
)

organization5 = users.Organization(
    name="Solar Power Initiative",
    email="info@solarpower.org",
    phone="444-555-6666",
    address="Pittsburgh, PA",
    resources=["solar panels", "batteries", "charging stations"],
    quantity=[20, 50, 10],
    time=12
)

companies.add(company1)
companies.add(company2)
companies.add(company3)
companies.add(company4)
companies.add(company5)
orgs.add(organization1)
orgs.add(organization2)
orgs.add(organization3)
orgs.add(organization4)
orgs.add(organization5)