# Shawn Adams
# 11 Dec 2023
# .exe icon by Eucalyp at https://www.flaticon.com/authors/eucalyp
import traceback

from PySimpleGUI import Window, Multiline, Button, InputText, theme, Text, Listbox
from sympy import solve, sympify, Eq

# def solve_eq(eq_txt, solve_sym_txt):
#     # Split into left and right side and sympify
#     left_txt = eq_txt.split('=')[0]
#     right_txt = eq_txt.split('=')[1]
#
#     # Create equation from sympify-ed left and right side
#     exp = Eq(sympify(left_txt), sympify(right_txt))
#     solve_sym = sympify(solve_sym_txt)
#     return solve(exp, solve_sym)


# def get_symbols(eq_txt):
#     window['solution'].update('')
#
#     # Split into left and right side and sympify
#     left_txt = eq_txt.split('=')[0]
#     right_txt = eq_txt.split('=')[1]
#
#     # Collect list of symbols from left and right side
#     all_symbols = sympify(right_txt).free_symbols
#     all_symbols = all_symbols.union(sympify(left_txt).free_symbols)
#
#     return list(all_symbols)


# PySimpleGUI constructor
theme('DarkGreen6')  # Add a touch of color
# Define window layout. Use key option to identify the value.
width = 40
layout = [[Text('Enter expression')],
          [InputText(default_text='y=a*x**2+b*x+c', size=(width, 5), key='exp')],
          [Button('Solve', key='solve_button')],
          [Text("Solve for: ")],
          [Listbox(['x'], size=(10, 5), key='solve_for', enable_events=True, select_mode=0), Button('Close')],
          [Multiline(size=(width, 5), auto_size_text=True, key='solution')]]

# Create the Window
window = Window('Equation Solver', layout).Finalize()
window['exp'].bind("<Return>", "_return")
window['solve_for'].bind("<Return>", "_return")

error_txt = 'solution'
invalid_syms = ['S', 'N', 'O', 'Q']
solve_for_index = 0

if __name__ == "__main__":
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        try:
            event, values = window.read()
            print(event)

            # if user closes window or clicks cancel
            if event in (None, 'Close'):
                break

            # when an item in the solve-for list is selected
            # if event == 'solve_for':
            #     print(window['solve_for'].GetIndexes()[0])
            #     solve_for_index = window['solve_for'].GetIndexes()[0]
            #     window['solve_button'].click()

            if event == 'Solve' or event == 'solve_for_return' or event == 'solve_button' or event == 'exp_return' \
                    or event == 'solve_for':

                # check for reserved symbols
                valid = not any(char in invalid_syms for char in values['exp'])

                if not valid:
                    err_syms = [char for char in values['exp'] if char in invalid_syms]
                    window[error_txt].update(f"Cannot use reserved symbols: {err_syms}")

                else:

                    solve_for_index = window['solve_for'].GetIndexes()[0]

                    print(solve_for_index)
                    # symbols = get_symbols(values['exp'])
                    eq_txt = values['exp']

                    # Split into left and right side and sympify
                    left_txt = eq_txt.split('=')[0]
                    right_txt = eq_txt.split('=')[1]

                    # Create equation from sympify-ed left and right side
                    exp = Eq(sympify(left_txt), sympify(right_txt))

                    # Collect list of symbols from left and right side
                    symbols = sympify(right_txt).free_symbols
                    symbols = symbols.union(sympify(left_txt).free_symbols)

                    # populate solve-for list
                    # window['solve_for'].update(values=list(symbols), set_to_index=solve_for_index)
                    window['solve_for'].update(values=list(symbols), set_to_index=solve_for_index)

                    # print(window['solve_for'].GetIndexes()[0])
                    solve_for_index = window['solve_for'].GetIndexes()[0]
                    # solve the expression
                    # print(sympify(list(symbols)[solve_for_index]))
                    solution = solve(exp, sympify(list(symbols)[solve_for_index]))

                    # solve_for_index = window['solve_for'].GetIndexes()[0]
                    # pprint(solution)
                    # window['img'].update(data=render_latex_to_image(latex(solution)))

                    window['solution'].update('')  # clear solution textbox

                    # print out all solutions

                    for i in range(len(solution)):
                        print(f"{i}: {solution[i]}")
                        # window['solution'].update(str(values['solve_for'][0]) + ' = ' + str(solution[i]) + '\n\n',
                        # append=True)

        # TODO: add pretty printing

        except IndexError as e:
            print(f"Index Error: {e}")
            print(f"{traceback.format_exc()}")
            window[error_txt].update(f"Formula parsing error: {e}\n{traceback.format_exc()}")

    window.close()
