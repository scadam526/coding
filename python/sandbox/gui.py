import sympy
from PySimpleGUI import Window, Multiline, Button, InputText, theme, Text
from sympy import symbols, solve, sympify

theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [[Text('Enter expression')],
          [InputText(default_text='Vfb=Vs*(Rb/(Rb+Rt)', size=(50, 5), key='textbox')],
          [Button('Ok'), Button('Close Window')]]  # identify the multiline via key option

# Create the Window
window = Window('Test', layout).Finalize()
# window.Maximize()
Vs, Vfb, Rb, Rt = symbols('Vs Vfb Rb Rt')
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'):  # if user closes window or clicks cancel
        break
    # print('You entered in the textbox:')
    # print(values['textbox'])  # get the content of multiline via its unique key
    equation = values['textbox']
    left_side, right_side = equation.split('=')

    # Remove leading and trailing whitespaces
    left = left_side.strip()
    right = right_side.strip()
    print(type(left))
    print(type(right))
    expr = sympy.Eq(left, right)
    sol = solve(expr, Vs)

window.close()
