from zibopt import scip
solver = scip.solver()

# All variables have default lower bounds of 0
x1 = solver.variable(scip.CONTINUOUS)
x2 = solver.variable(scip.CONTINUOUS)

# x1 has an upper bound of 2
solver += x1 >= 0
solver += x2 >= 0

solver += 2*x1 + x2 <= 4

# Add a constraint such that:  x1 + x2 + 3*x3**2 <= 3
solver += x1 + 2*x2 <= 3

# The objective function is: z = x1*x2 + x2 + 2*x3
solution = solver.maximize(objective=x1 + x2)

# Print the optimal solution if it is feasible.
if solution:
    print('z  =', solution.objective)
    print('x1 =', solution[x1])
    print('x2 =', solution[x2])
else:
    print('invalid problem')
