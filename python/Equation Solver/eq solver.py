from sympy import *
import sys

# create a class for the sympy equation
class Equation:
    def __init__(self, eq_txt):
        self.eq_txt = eq_txt
        self.lhs = sympify(eq_txt.split("=")[0])
        self.rhs = sympify(eq_txt.split("=")[1])
        self.expression = Eq(self.lhs, self.rhs)
        self.symbols = self.lhs.free_symbols.union(self.rhs.free_symbols)
        self.sym_list = list(self.symbols)
    
    def solve_for(self, sym):
        self.solution = solve(self.expression, sym)
        return self.solution

if __name__ == "__main__":
    
    # if no arguments are given, ask for an equation
    if len(sys.argv) == 1:
        eq = Equation(input("Enter an equation: "))
        eq.solve_for(input("Enter solve for symbol: "))
    # if there is one argument, use that as the equation and ask for a solve-for symbol
    elif len(sys.argv) == 2:
        eq = Equation(sys.argv[1])
        eq.solve_for(input("Enter solve for symbol: "))
    # if there are two arguments use the first as the equation and the sencond as the symbol to solve for
    elif len(sys.argv) == 3:
        eq = Equation(sys.argv[1])
        pprint(eq.solve_for(sys.argv[2]))
    else:
        print("Error: Invlaid arguments")

    pprint(eq.solution)
