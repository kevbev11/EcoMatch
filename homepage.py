from nicegui import ui
import users

#companies = []
#organizations = []
#userData = {"role": None, "name": "", "address": "", "resources": [], "days": None}

#mainpage

@ui.page('/profile')
def profile():
    with ui.card():
        name = ui.input(label='Name', placeholder='start typing', value = '')
        email = ui.input(label='Email', placeholder='example@gmail.com')
        phone = ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX')
        address = ui.input(label='Address', placeholder='start typing')
        city = ui.input(label='City', placeholder='ex. Danville')
        state = ui.input(label='State', placeholder='ex. CA')
        zip_code = ui.input(label='Zip Code', placeholder='start typing')
        time = ui.input(label='When?', placeholder='start typing')
        quantity = ui.input(label='How many?', placeholder='start typing')
        

ui.label('I am a . . .').style('color: #88c5d8; font-size: 600%; font-weight: 300')
with ui.button_group():
        ui.button('Company', on_click=lambda: ui.navigate.to('/profile'), color = "#88c5d8").style('font-size: 100px; margin-right: 100px;')
        ui.button('Organization', on_click=lambda: ui.navigate.to('/profile'), color = "#88c5d8").style('font-size: 100px')


ui.run()