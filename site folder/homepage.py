from nicegui import ui

#companies = []
#organizations = []
#userData = {"role": None, "name": "", "address": "", "resources": [], "days": None}

#mainpage

@ui.page('/other_page')
def other_page():
    ui.label('this is the other page')

with ui.button_group():
    ui.button('Company', on_click=lambda: ui.navigate.to('/other_page'), color = 'yellow').style('font-size: 100px').props('outline')
    ui.button('Organization', on_click=lambda: ui.navigate.to('/other_page')).style('font-size: 100px')

ui.run()