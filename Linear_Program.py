from gurobipy import *
import numpy as np

# Define the two models:
opt_model = Model(name="linear program")
opt_model_dual = Model(name="linear program dual")

# This is for the problem:
# max 4x1 + 3x2 + 4x3
# 3x1 + 2x2 + x3 <= 8
# 2x1 + 2x2 + 2x3 <= 9
# 4x1 + 5x2 + 2x3 <= 10
# x1,x2,x3>=0

""" Change the values here: """
# Non-negativity constraints:
# lb = lower bound, ub = upper bound, inf = float('inf')
x1 = opt_model.addVar(name='x1', vtype=GRB.CONTINUOUS, lb=0)
x2 = opt_model.addVar(name='x2', vtype=GRB.CONTINUOUS, lb=0)
x3 = opt_model.addVar(name='x3', vtype=GRB.CONTINUOUS, lb=0)

# Constraints:
c1 = opt_model.addConstr(3 * x1 + 2 * x2 + x3 <= 8, name="c1")
c2 = opt_model.addConstr(2 * x1 + 2 * x2 + 2 * x3 <= 9, name="c2")
c3 = opt_model.addConstr(4 * x1 + 5 * x2 + 2 * x3 <= 10, name="c3")

# RHS of constraints only if needed to calculate optimal dual variable
b = np.array([8, 9, 10])

# Objective Function
obj_fn = 4*x1 + 3*x2 + 4*x3
# Set MAXIMIZE OR MINIMIZE
opt_model.setObjective(obj_fn, GRB.MAXIMIZE)

"""Here come the calculations """

# Calculation:

# Normal Problem
opt_model.optimize()
opt_model.write('linear_model.lp')
print("\n #### Solution Primal ####")
print(f'Optimal objective function Value: {opt_model.objVal}')
for v in opt_model.getVars():
    print(f"{v.varName}: {v.x}")

# Dual Problem
print("\n ## Solution dualvariables / Shadow Prices yi ###")

# Calculates optimal value of the dual problem:
sum = 0
for index, y in enumerate(opt_model.getAttr(GRB.Attr.Pi)):
    sum = sum + y * b[index]
print(f"The optimal dual variable is {sum}")

for i, y in enumerate(opt_model.getAttr(GRB.Attr.Pi)):
    print(f"y{i + 1}: {y}")

if sum == opt_model.objVal:
    print("We have strong duality =")
if opt_model.objVal <= sum:
    print("We have weak duality <=")

# Sensitivity Analysis
print("\n### Sensitivity Analyis ###")
print("Sensitivity Analysis of the Objective Function")
print(
    "X=Final Value, RC = Reduced Cost, OBJ = Coefficient,Allowable Increase = SAObjup-OBj, Allowable Decrease = Obj - SAObjLow "
    "Decrease")
opt_model.printAttr(['X', 'RC', 'Obj', 'SAObjUp', 'SAObjLow'])

print("\n Sensitity Analyis of the Constraints")
print("Pi = Shadow Price, Allowable Increase = SARHSUp - RHS, Allowable Decrease = RHS - SAHRSLow")
opt_model.printAttr(["Sense", "Slack", "Pi", "RHS", "SARHSUp", "SARHSLow"])
