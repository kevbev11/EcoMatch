from nicegui import ui

#companies = []
#organizations = []
#userData = {"role": None, "name": "", "address": "", "resources": [], "days": None}

#def homepage():
ui.button('Company', on_click=lambda: ui.open('https://www.google.com/maps'))

ui.run()