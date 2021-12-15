from gurobipy import *
import numpy as np

# Theory:
"""
n assignees to be assigned to n different tasks 
Each assignment has a certain cost cij (i = assignee, j = task)
Problem: Find the best assignment of all tasks that minimize the total cost 

Constraints:
1. |assignees| = |tasks| = n
2. each assignee is to be assigned to exactly one task
3. each task is to be assigned to exactly one assignee
"""
model = Model(name="assignment problem")
M = GRB.INFINITY

# Define the assignees and tasks:
cost = np.array([[820, 810, 840, 960, 0],
                 [820, 810, 840, 960, 0],
                 [800, 870, M, 920, 0],
                 [800, 870, M, 920, 0],
                 [740, 900, 810, 840, M]])

# Creating Variables:
# x[i, j] is an array of binary variables (1 -> assignee i is assigned to task j) otherwise 0
x = {}
for i in range(cost.shape[0]):
    for j in range(cost.shape[0]):
        x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x[{i},{j}]")
model.update()

# We add our first constraint:
# 1. Each assignee is assigned to exactly one task!
for i in range(cost.shape[0]):
    model.addConstr(1 == quicksum(x[i, j] for j in range(cost.shape[1])), name=f"assignee_to_task_{i}")

# 2. Each task has exactly one assignee assigned to it:
for j in range(cost.shape[1]):
    model.addConstr(1 == quicksum(x[i, j] for i in range(cost.shape[0])), name=f"task_to_assignee_{j}")
model.update()

# Creating the objective function: sum(i=1 to n) sum(j=1 to n) cij*xij
model.setObjective(quicksum(quicksum(x[i, j] * cost[i][j] for i in range(cost.shape[0])) for j in range(cost.shape[1])),
                   GRB.MINIMIZE)
model.getObjective()
model.optimize()

print("## Solution ##")
print(f'Optimal objective function Value: {model.objVal}')
for v in model.getVars():
    Matrix = np.zeros((cost.shape[0], cost.shape[1]))

    print(Matrix)
    print(f"{v.varName}: {v.x}")
