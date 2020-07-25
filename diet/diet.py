from mip import Model, xsum, minimize, INTEGER
import pandas as pd

model = Model("Diet")
table = r'table.csv'
df = pd.read_csv(table)

# Variables
X = [model.add_var(name=row['name'], var_type=INTEGER, lb=0, ub=row['max_serv']) for i, row in df.iterrows()]

def constraint_vars(attr):
    return (row[attr] * X[i] for i, row in df.iterrows())

#
# Objective function
#
model.objective = minimize(xsum(constraint_vars('price')))

#
# Constraints
#

# Energy
model += xsum(constraint_vars('energy')) >= 1000

# Protein
model += xsum(constraint_vars('protein')) >= 55

# Calcium
model += xsum(constraint_vars('calcium')) >= 800

model.optimize()

print('Solution\tVar(x)')
print('-'*24)
for v in model.vars:
    print(f'{v.x}\t{v}')
