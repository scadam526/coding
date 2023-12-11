from sympy import sympify, solve, Eq, pprint

# Example equations
# Vfb = Vs * (Rb / (Rb + Rt))
# y = a*x**2+b*x+c

# prompt for equation
equation_string = input("Enter equation (<left side = right side>) : ")

# Split into left and right side and sympify
leftTxt = equation_string.split('=')[0]
rightTxt = equation_string.split('=')[1]

# Create equation from sympify-ed left and right side
expression = Eq(sympify(leftTxt), sympify(rightTxt))

# Collect list of symbols from left and right side
all_symbols = sympify(rightTxt).free_symbols
all_symbols = all_symbols.union(sympify(leftTxt).free_symbols)

# turn symbols into a list
declared_symbols = list(all_symbols)

# print available symbols and prompt for solve-for symbol
print(f"Symbols: {declared_symbols}\n")
solve_sym = sympify(input(f"Enter solve-for symbol: "))

# solve and print
solution = solve(expression, solve_sym)
pprint(solution)
