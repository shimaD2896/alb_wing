import sympy as sp
# variables
x,y=sp.symbols('x y')
f1 = x**2 + x*y + sp.Rational(1,4)
f2 = y + 3*x*y**2
sol=sp.solve([f1,f2],[x,y], dict=True)
sol


# numeric solve Newton from initial (1.5,3.5)
xn, yn = 1.5, 3.5
def f(x,y): return x**2 + x*y + 0.25
def g(x,y): return y + 3*x*y**2
def J(x,y):
    return sp.Matrix([[2*x+y, x],
                      [3*y**2, 1+6*x*y]])
xv, yv = xn, yn
for i in range(10):
    F = sp.Matrix([f(xv,yv), g(xv,yv)])
    Jinv = J(xv,yv).inv()
    corr = Jinv*F
    xv, yv = float(xv - corr[0]), float(yv - corr[1])
xv, yv

print(sol, (xv, yv))

