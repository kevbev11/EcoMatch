from nicegui import ui

#companies = []
#organizations = []
#userData = {"role": None, "name": "", "address": "", "resources": [], "days": None}

#mainpage

@ui.page('/other_page')
def other_page():
    ui.label('this is the other page')

ui.label('I am a . . .')

with ui.button_group():
    ui.button('Company', on_click=lambda: ui.navigate.to('/other_page'), color = "#88c5d8").style('font-size: 100px; margin-right: 50px;')
    ui.button('Organization', on_click=lambda: ui.navigate.to('/other_page'), color = "#88c5d8").style('font-size: 100px')

ui.run()