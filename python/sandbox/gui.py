from PySimpleGUI import Window, Multiline, Button, InputText, theme, Text
from sympy import solve, sympify, Eq, pprint


def solve_eq(eq_txt, solve_sym_txt):
    # Split into left and right side and sympify
    left_txt = eq_txt.split('=')[0]
    right_txt = eq_txt.split('=')[1]

    # Create equation from sympify-ed left and right side
    exp = Eq(sympify(left_txt), sympify(right_txt))
    solve_sym = sympify(solve_sym_txt)
    return solve(exp, solve_sym)


def get_symbols(eq_txt):
    # Split into left and right side and sympify
    left_txt = eq_txt.split('=')[0]
    right_txt = eq_txt.split('=')[1]

    # Collect list of symbols from left and right side
    all_symbols = sympify(right_txt).free_symbols
    all_symbols = all_symbols.union(sympify(left_txt).free_symbols)

    return list(all_symbols)


def update_sym_text(target_key, src_key):
    window[target_key].update("Available symbols: " + " ".join(str(item) for item in get_symbols(values[src_key])))


# PySimpleGUI constructor
theme('DarkGreen6')  # Add a touch of color
# Define window layout. Use key option to identify the value.
width = 40
layout = [[Text('Enter expression')],
          [InputText(default_text='y=a*x**2+b*x+c', size=(width, 5), key='exp')],
          [Text("Available symbols: ", key='sym_txt')],
          [Text('Solve for:  '), InputText(default_text='x', size=(5, 5), key='solve_for')],
          [Button('Parse'), Button('Solve'), Button('Close')],
          [Multiline(size=(width, 5), auto_size_text=True, key='sol')]]

# Create the Window
window = Window('Equation Solver', layout).Finalize()
window['exp'].bind("<Return>", "_return")
window['solve_for'].bind("<Return>", "_return")

# Event Loop to process "events" and get the "values" of the inputs
while True:
# TODO add basic error handling
    event, values = window.read()
    print(event)
    if event in (None, 'Close'):  # if user closes window or clicks cancel
        break

    if event == 'Parse' or event == 'exp_return':  # if user closes window or clicks cancel
        update_sym_text('sym_txt', 'exp')

    if event == 'Solve' or event == 'solve_for_return':  # if user closes window or clicks cancel
        update_sym_text('sym_txt', 'exp')
        solution = solve_eq(values['exp'], values['solve_for'])
        pprint(solution)
        window['sol'].update('')
        for i in range(len(solution)):
            window['sol'].update(values['solve_for'] + ' = ' + str(solution[i]) + '\n\n', append=True)
# TODO: add pretty printing
window.close()
