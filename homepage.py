from nicegui import ui
import users
import data
from datetime import datetime
import time
import threading
import matching

label = ui.label("I am a.").style('color: #88c5d8; font-size: 800%; font-weight: 1000').style('position: absolute; top: 25%; left: 50%; transform: translate(-50%, -50%);')

def animate_ellipsis():
    count = 0
    def update_label():
        nonlocal count
        if count == 0:
            label.set_text("I am a.")
        elif count == 1:
            label.set_text("I am a..")
        elif count == 2:
            label.set_text("I am a...")
        count = (count + 1) % 3
    ui.timer(0.5, update_label)
animate_ellipsis()

#mainpage
with ui.column().classes('absolute-center items-center'):
    #ui.label('I am a . . .').style('color: #88c5d8; font-size: 800%; font-weight: 1000')
    with ui.row().classes('justify-center items-center gap-4'):
        ui.button('company', on_click=lambda: ui.navigate.to('/company_profile'), color="#88c5d8").style('font-size: 400%;').props('rounded')
        ui.button('organization', on_click=lambda: ui.navigate.to('/org_profile'), color="#88c5d8").style('font-size: 400%;').props('rounded')
        # test for no match page: ui.button('no match', on_click=lambda: ui.navigate.to('/no_match'), color="#88c5d8").style('font-size: 400%;').props('rounded')
        #ui.button('org match view', on_click=lambda: ui.navigate.to('/org_match_view'), color="#88c5d8").style('font-size: 400%;').props('rounded')
        #ui.button('company match view', on_click=lambda: ui.navigate.to('/company_match_view'), color="#88c5d8").style('font-size: 400%;').props('rounded')

@ui.page('/org_match_view')
def org_match_view():
    # Ensure `currOrg` and `companies` are valid
    if data.currOrg is None or not hasattr(data.currOrg, "resources"):
        ui.notify("No organization data available.")
        return

    currOrg = data.currOrg
    if not data.companies:
        ui.notify("No companies data available.")
        return

    # Initialize matcher
    matcher = matching.SemanticMatcher(companies=data.companies, organizations=[currOrg])
    matches = matcher.find_matches(similarity_threshold=-1.0, max_matches=3)

    # Debug: Print matches
    print(f"Matches: {matches}")

    # Define dialog for details
    with ui.dialog() as dialog, ui.card():
        details_label = ui.label()
        score_label = ui.label()
        ui.button('Close', on_click=dialog.close)

    def open_dialog(company, org, score):
        details_label.text = f"Company: {company} matched with {org}"
        score_label.text = f"Match Score: {score:.2f}"
        dialog.open()

    # Render UI cards for matches
    for company, org, score in matches:
        with ui.card():
            ui.label(f"Company: {company}")
            ui.label(f"Matched Organization: {org}")
            ui.label(f"Match Score: {score:.2f}")
            ui.button(
                'View Details',
                on_click=lambda c=company, o=org, s=score: open_dialog(c, o, s)
            )

@ui.page('/company_match_view')  # Displays organizations matched with the current company
def company_match_view():
    # Ensure `currComp` is set
    if data.currComp is None or not hasattr(data.currComp, "resources"):
        ui.notify("No current company data available.")
        return

    currComp = data.currComp
    if not data.orgs:
        ui.notify("No organizations data available.")
        return

    # Initialize matcher with the current company and all organizations
    matcher = matching.SemanticMatcher(companies=[currComp], organizations=data.orgs)
    matches = matcher.find_matches(similarity_threshold=-1.0, max_matches=3)

    # Debug: Print matches
    print(f"Matches: {matches}")

    # Define dialog for details
    with ui.dialog() as dialog, ui.card():
        details_label = ui.label()
        score_label = ui.label()
        ui.button('Close', on_click=dialog.close)

    def open_dialog(org, company, score):
        details_label.text = f"Organization: {org} matched with {company}"
        score_label.text = f"Match Score: {score:.2f}"
        dialog.open()

    # Render UI cards for matches
    for org, company, score in matches:
        with ui.card():
            ui.label(f"Organization: {org}")
            ui.label(f"Matched Company: {company}")
            ui.label(f"Match Score: {score:.2f}")
            ui.button(
                'View Details',
                on_click=lambda o=org, c=company, s=score: open_dialog(o, c, s)
            )

#Displays that there is no match for a company or organization
@ui.page('/no_match')
def no_match():
    with ui.column().classes('absolute-center items-center'):
        ui.label('No matches found yet. Please check back later when more businesses have registered.').style('color: #88c5d8; font-size: 400%; font-weight: 300')

#Creating a company profile
@ui.page('/company_profile')
def company_profile():
    resources = []
    quantity = []
    with ui.column().classes('absolute-center items-center'):
        with ui.row().classes('justify-center items-center gap-4'):
            with ui.card().classes('w-[600px]'):
                # Static inputs inside the card
                name = ui.input(label='Name', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]')
                email = ui.input(label='Email', placeholder='example@gmail.com', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]')
                phone = ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]')
                address = ui.input(label='Address', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]')

                # Date picker with menu
                with ui.input(label='Date') as date:
                    with ui.menu().props('no-parent-event') as menu:
                        with ui.date().bind_value(date).classes():
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=menu.close).props('flat')
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer w-[560px]')

                # Number input for dynamic fields
                num = ui.number(label='Number', value=1, validation={'Must Be Positive': lambda value: value > 0}).classes('w-[565px]')

                # A container to hold dynamically added inputs, placed **inside the card**
                with ui.column() as container:
                    pass

                # Function to dynamically create inputs
                def create_inputs():
                    nonlocal resources, quantity
                    container.clear()  # Clear existing inputs in the container
                    resources.clear()  # Clear stored resource references
                    quantity.clear()

                    try:
                        count = int(num.value)
                        for i in range(count):
                            with container:  # Add inputs to the container
                                with ui.row().classes('items-center'):  # Side-by-side layout
                                    resource = ui.input(label=f'Resource {i + 1}', placeholder='Enter name', validation={'Must Not Be Empty': lambda value: len(value) > 0})
                                    amount = ui.number(label='Amount', value=1, validation={'Must Be Positive': lambda value: value > 0})
                                    resources.append(resource.value)  # Store each input for later use
                                    quantity.append(amount.value)
                    except ValueError:
                        ui.notify('Please enter a valid positive number.')

                # Button to trigger dynamic input creation
                ui.button('Add Resources', on_click=create_inputs)

                # Function to save data into a Company object
                def save_data():
                    # Collect data from inputs
                    if not all([name.value, email.value, phone.value, address.value, date.value]):
                        ui.notify("You still have one or more blanks to fill.")
                        return

                    if not(r for r in resources):
                        ui.notify("Please fill in all resource fields.")
                        return
                    
                    time = days_between_dates(date.value)

                    data.currComp = users.Company(name.value, email.value, phone.value, address.value, [r for r in resources], [q for q in quantity], time)

                    data.companies.add(users.Company(name.value, email.value, phone.value, address.value, [r for r in resources], [q for q in quantity], time))
                    
                    # Display or process the Company object
                    ui.notify(f"Company saved: {name}")
                
                def navigate():
                    if not all([name.value, email.value, phone.value, address.value, date.value]) or not(r for r in resources):
                        ui.notify("You still have one or more blanks to fill.")
                        return
                    if data.orgs == set(): ui.navigate.to('/no_match')
                    else: ui.navigate.to('/company_match_view')
                
                ui.button('Save', on_click=save_data)
                ui.button('Find Match!', on_click=navigate)

#Creating an organization profile
@ui.page('/org_profile')
def org_profile():
    resources = []
    quantity = []
    with ui.column().classes('absolute-center items-center'):
        with ui.row().classes('justify-center items-center gap-4'):
            with ui.card().classes('w-[600px]'):
                # Static inputs inside the card
                name = ui.input(label='Name', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]')
                email = ui.input(label='Email', placeholder='example@gmail.com', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]')
                phone = ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]')
                address = ui.input(label='Address', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]')

                # Date picker with menu
                with ui.input(label='Date') as date:
                    with ui.menu().props('no-parent-event') as menu:
                        with ui.date().bind_value(date):
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=menu.close).props('flat')
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer w-[560px]')

                # Number input for dynamic fields
                num = ui.number(label='Number', value=1, validation={'Must Be Positive': lambda value: value > 0}).classes('w-[565px]')

                # A container to hold dynamically added inputs, placed **inside the card**
                with ui.column() as container:
                    pass

                # Function to dynamically create inputs
                def create_inputs():
                    nonlocal resources, quantity
                    container.clear()  # Clear existing inputs in the container
                    resources.clear()  # Clear stored resource references
                    quantity.clear()

                    try:
                        count = int(num.value)
                        for i in range(count):
                            with container:  # Add inputs to the container
                                with ui.row().classes('items-center'):  # Side-by-side layout
                                    resource = ui.input(label=f'Resource {i + 1}', placeholder='Enter name', validation={'Must Not Be Empty': lambda value: len(value) > 0})
                                    amount = ui.number(label='Amount', value=1, validation={'Must Be Positive': lambda value: value > 0})
                                    resources.append(resource.value)  # Store each input for later use
                                    quantity.append(amount.value)
                    except ValueError:
                        ui.notify('Please enter a valid positive number.')

                # Button to trigger dynamic input creation
                ui.button('Add Resources', on_click=create_inputs)

                # Function to save data into a Company object
                def save_data():
                    # Collect data from inputs
                    if not all([name.value, email.value, phone.value, address.value, date.value]):
                        ui.notify("You still have one or more blanks to fill.")
                        return

                    if not(r for r in resources):
                        ui.notify("Please fill in all resource fields.")
                        return
                    
                    time = days_between_dates(date.value)
                    
                    data.currOrg = users.Organization(name.value, email.value, phone.value, address.value, [r for r in resources], [q for q in quantity], time)

                    data.orgs.add(users.Organization(name.value, email.value, phone.value, address.value, [r for r in resources], [q for q in quantity], time))
                    
                    # Display or process the Company object
                    ui.notify(f"Organization saved: {name}")
                
                def navigate():
                    if not all([name.value, email.value, phone.value, address.value, date.value]) or not(r for r in resources):
                        ui.notify("You still have one or more blanks to fill.")
                        return
                    if data.companies == set(): ui.navigate.to('/no_match')
                    else: ui.navigate.to('/org_match_view')

                ui.button('Save', on_click=save_data)
                ui.button('Find Match!', on_click=navigate)

def days_between_dates(date: str) -> int: #Calculate the number of days between future date and today.
    try:
        d1 = datetime.now()  # Current date
        d2 = datetime.strptime(date, "%Y-%m-%d")  # Convert input string to datetime
        return abs((d2 - d1).days)  # Return the absolute difference in days
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date}. Expected format is YYYY-MM-DD.") from e

ui.run()