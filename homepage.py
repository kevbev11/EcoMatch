from nicegui import ui
import users
import data

#mainpage
with ui.column().classes('absolute-center items-center'):
    ui.label('I am a . . .').style('color: #88c5d8; font-size: 800%; font-weight: 1000')
    with ui.row().classes('justify-center items-center gap-4'):
        ui.button('company', on_click=lambda: ui.navigate.to('/company_profile'), color="#88c5d8").style('font-size: 400%;').props('rounded')
        ui.button('organization', on_click=lambda: ui.navigate.to('/org_profile'), color="#88c5d8").style('font-size: 400%;').props('rounded')
        # test for no match page: ui.button('no match', on_click=lambda: ui.navigate.to('/no_match'), color="#88c5d8").style('font-size: 400%;').props('rounded')
        
@ui.page('/no_match')
def no_match():
    with ui.column().classes('absolute-center items-center'):
        ui.label('No matches found yet. Please check back later when more businesses have registered.').style('color: #88c5d8; font-size: 400%; font-weight: 300')

@ui.page('/company_profile')
def company_profile():
    resources = []
    quantity = []
    with ui.column().classes('absolute-center items-center'):
        with ui.row().classes('justify-center items-center gap-4'):
            with ui.card().classes('w-[600px]'):
                # Static inputs inside the card
                name = ui.input(label='Name', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]').value
                email = ui.input(label='Email', placeholder='example@gmail.com', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]').value
                phone = ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]').value
                address = ui.input(label='Address', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]').value

                # Date picker with menu
                with ui.input(label='Date') as date:
                    with ui.menu().props('no-parent-event') as menu:
                        with ui.date().bind_value(date).classes():
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=menu.close).props('flat')
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer w-[560px]')
                    time = date

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
                                    resource = ui.input(label=f'Resource {i + 1}', placeholder='Enter name', validation={'Must Not Be Empty': lambda value: len(value) > 0}).value
                                    amount = ui.number(label='Amount', value=1, validation={'Must Be Positive': lambda value: value > 0}).value
                                    resources.append(resource)  # Store each input for later use
                                    quantity.append(amount)
                    except ValueError:
                        ui.notify('Please enter a valid positive number.')

                # Button to trigger dynamic input creation
                ui.button('Add Resources', on_click=create_inputs)

                # Function to save data into a Company object
                def save_data():
                    # Collect data from inputs
                    if not name or not email or not phone or not address or not date.value or not (r.value for r in resources) or not (q.value for q in quantity):
                        ui.notify(f"You still have one or more blanks to fill")
                        return
                    
                    data.companies.add(users.Company(name, email, phone, address, [r.value for r in resources], [q.value for q in quantity], date.value))
                    
                    # Display or process the Company object
                    ui.notify(f"Company saved: {name}")
                
                ui.button('Save', on_click=save_data)

@ui.page('/org_profile')
def org_profile():
    resources = []
    quantity = []
    with ui.column().classes('absolute-center items-center'):
        with ui.row().classes('justify-center items-center gap-4'):
            with ui.card().classes('w-[600px]'):
                # Static inputs inside the card
                name = ui.input(label='Name', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]').value
                email = ui.input(label='Email', placeholder='example@gmail.com', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]').value
                phone = ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]').value
                address = ui.input(label='Address', placeholder='start typing', validation={'Must Not Be Empty': lambda value: len(value) > 0}).classes('w-[565px]').value

                # Date picker with menu
                with ui.input(label='Date') as date:
                    with ui.menu().props('no-parent-event') as menu:
                        with ui.date().bind_value(date):
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=menu.close).props('flat')
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer w-[560px]')
                    time = date

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
                                    resource = ui.input(label=f'Resource {i + 1}', placeholder='Enter name', validation={'Must Not Be Empty': lambda value: len(value) > 0}).value
                                    amount = ui.number(label='Amount', value=1, validation={'Must Be Positive': lambda value: value > 0}).value
                                    resources.append(resource)  # Store each input for later use
                                    quantity.append(amount)
                    except ValueError:
                        ui.notify('Please enter a valid positive number.')

                # Button to trigger dynamic input creation
                ui.button('Add Resources', on_click=create_inputs)

                # Function to save data into a Company object
                def save_data():
                    # Collect data from inputs
                    if not name or not email or not phone or not address or not date.value or not (r.value for r in resources) or not (q.value for q in quantity):
                        ui.notify(f"You still have one or more blanks to fill")
                        return
                    
                    data.orgs.add(users.Organization(name, email, phone, address, [r.value for r in resources], [q.value for q in quantity], date.value))
                    
                    # Display or process the Company object
                    ui.notify(f"Organization saved: {name}")
                
                ui.button('Save', on_click=save_data)

ui.run()