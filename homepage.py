from nicegui import ui
import users
import data

#mainpage
with ui.row().classes('items-center'):
    ui.label('I am a . . .').style('color: #88c5d8; font-size: 500%; font-weight: 300')
    with ui.button_group():
        ui.button('Company', on_click=lambda: ui.navigate.to('/company_profile'), color = "#88c5d8").style('font-size: 100px; margin-right: 100px;')
        ui.button('Organization', on_click=lambda: ui.navigate.to('/org_profile'), color = "#88c5d8").style('font-size: 100px')

@ui.page('/company_profile')
def company_profile():
    resources = []
    quantity = []

    with ui.card():
        # Static inputs inside the card
        name = ui.input(label='Name', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0})
        email = ui.input(label='Email', placeholder='example@gmail.com', validation={'Must Not Be Empty': lambda value: len(value) > 0})
        phone = ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX', validation={'Must Not Be Empty': lambda value: len(value) > 0})
        address = ui.input(label='Address', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0})

        # Date picker with menu
        with ui.input(label='Date') as date:
            with ui.menu().props('no-parent-event') as menu:
                with ui.date().bind_value(date):
                    with ui.row().classes('justify-end'):
                        ui.button('Close', on_click=menu.close).props('flat')
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
            time = date

        # Number input for dynamic fields
        num = ui.number(label='Number of Resources', value=1, validation={'Must Be Positive': lambda value: value > 0})

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
            if not all([name.value, email.value, phone.value, address.value, time.value]):
                ui.notify("You still have one or more blanks to fill.")
                return
            elif not (r for r in resources):
                ui.notify("Please fill in all resource fields.")
                return
            data.companies.add(users.Company(name.value, email.value, phone.value, address.value, [r for r in resources], [q for q in quantity], time.value))
            # Display or process the Company object
            ui.notify(f"Company saved: {name.value}")
            if data.orgs == set(): ui.navigate.to('/no_match')
            else: ui.navigate.to('/company_matches')
        
        ui.button('Save', on_click=save_data)

@ui.page('/org_profile')
def org_profile():
    resources = []
    quantity = []

    with ui.card():
        # Static inputs inside the card
        name = ui.input(label='Name', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0})
        email = ui.input(label='Email', placeholder='example@gmail.com', validation={'Must Not Be Empty': lambda value: len(value) > 0})
        phone = ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX', validation={'Must Not Be Empty': lambda value: len(value) > 0})
        address = ui.input(label='Address', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0})

        # Date picker with menu
        with ui.input(label='Date') as date:
            with ui.menu().props('no-parent-event') as menu:
                with ui.date().bind_value(date):
                    with ui.row().classes('justify-end'):
                        ui.button('Close', on_click=menu.close).props('flat')
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
            time = date

        # Number input for dynamic fields
        num = ui.number(label='Number', value=1, validation={'Must Be Positive': lambda value: value > 0})

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
            if not all([name.value, email.value, phone.value, address.value, time.value]):
                ui.notify("You still have one or more blanks to fill.")
                return
            elif not (r for r in resources):
                ui.notify("Please fill in all resource fields.")
                return
            
            data.orgs.add(users.Organization(name.value, email.value, phone.value, address.value, [r for r in resources], [q for q in quantity], time.value))
            
            # Display or process the Company object
            ui.notify(f"Organization saved: {name.value}")

            if data.companies == set(): ui.navigate.to('/no_match')
            else: ui.navigate.to('/org_matches')
        
        ui.button('Save', on_click=save_data)

ui.run()