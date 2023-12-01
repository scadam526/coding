from sympy import sympify, solve, Eq

# Example equation string
# equation_string = "Vfb = Vs * (Rb / (Rb + Rt))"
# equation_string = "y = a*x**2+b*x+c"
equation_string = input("Enter equation (<left side = right side>) : ")

# Split into left and right side and sympify
leftTxt = equation_string.split('=')[0]
rightTxt = equation_string.split('=')[1]

# Create equation from sympify-ed left and right side
expression = Eq(sympify(leftTxt), sympify(rightTxt))

# Collect list of symbols from left and right side
all_symbols = sympify(rightTxt).free_symbols
all_symbols = all_symbols.union(sympify(leftTxt).free_symbols)
declared_symbols = list(all_symbols)
print(f"Symbols: {declared_symbols}\n", type(sympify('x')))

solve_sym = sympify(input(f"Enter solve-for symbol: "))
solution = solve(expression, solve_sym)
for i in solution:
    print(f"{solve_sym} = {i}")
