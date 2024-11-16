from nicegui import ui

ui.input(label='Name', placeholder='start typing',
         on_change=lambda e: result.set_text('you typed: ' + e.value))
ui.input(label='Email', placeholder='example@gmail.com',
         on_change=lambda e: result.set_text('you typed: ' + e.value))
ui.input(label='Phone Number', placeholder='(XXX) XXX-XXXX',
         on_change=lambda e: result.set_text('you typed: ' + e.value))
ui.input(label='Address', placeholder='start typing',
         on_change=lambda e: result.set_text('you typed: ' + e.value))
ui.input(label='City', placeholder='ex. Danville',
         on_change=lambda e: result.set_text('you typed: ' + e.value))
ui.input(label='State', placeholder='ex. CA',
         on_change=lambda e: result.set_text('you typed: ' + e.value))
ui.input(label='Zip Code', placeholder='start typing',
         on_change=lambda e: result.set_text('you typed: ' + e.value))
ui.input(label='When?', placeholder='start typing',
         on_change=lambda e: result.set_text('you typed: ' + e.value))
ui.input(label='How many?', placeholder='start typing',
         on_change=lambda e: result.set_text('you typed: ' + e.value))


result = ui.label()

ui.run()