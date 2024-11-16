from nicegui import ui
import users
import data

#companies = []
#organizations = []
#userData = {"role": None, "name": "", "address": "", "resources": [], "days": None}

#mainpage

@ui.page('/company_profile')
def company_profile():
    with ui.card():
        resources = []
        quantity = []
        name = ui.input(label='Name', placeholder='start typing')
        email = ui.input(label='Email', placeholder='example@gmail.com')
        phone = ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX')
        address = ui.input(label='Address', placeholder='start typing')
        city = ui.input(label='City', placeholder='ex. Danville')
        state = ui.input(label='State', placeholder='ex. CA')
        zip_code = ui.input(label='Zip Code', placeholder='start typing', validation={'Must be a number': lambda value: type(value) == int and value < 10**6})
        #time = ui.input(label='When?', placeholder='start typing')
        ui.label('When?')
        with ui.input('Date') as date:
            with ui.menu().props('no-parent-event') as menu:
                with ui.date().bind_value(date):
                    #time = ui.date().bind_value(date)
                    with ui.row().classes('justify-end'):
                        ui.button('Close', on_click=menu.close).props('flat')
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
            time = date
        # num = ui.number(label='Number', value=1, format='%.2f')
        # #num = ui.input(label='How many?', placeholder='start typing', validation={'Must be a number': lambda value: value.isdigit()})
        # for i in range(int(str(num))):
        #     resources.append(ui.input(label='Resource', placeholder='start typing'))
        #     quantity.append(ui.input(label='Quantity', placeholder='start typing', validation={'Must be a number': lambda value: type(value) == int}))
        
        # data.companies.add(users.Company(name, email, phone, address, zip_code, time))

with ui.column().classes('absolute-center items-center'):
    ui.label('I am a . . .').style('color: #88c5d8; font-size: 800%; font-weight: 1000')
    with ui.row().classes('justify-center items-center gap-4'):
        ui.button('company', on_click=lambda: ui.navigate.to('/company_profile'), color="#88c5d8").style('font-size: 400%;').props('rounded')
        ui.button('organization', on_click=lambda: ui.navigate.to('/org_profile'), color="#88c5d8").style('font-size: 400%;').props('rounded')


ui.run()