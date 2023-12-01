import sympy as sp

Rt, Rb, Vfb, Vin = sp.symbols('Rt, Rb, Vfb, Vin')
eq = sp.Eq(Vfb, (Vin*Rb)/(Rb+Rt))
sol = sp.solve(eq, Rb)
sp.init_printing()
print(type(Vfb))
print(sol)
