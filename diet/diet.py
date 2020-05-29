from mip import Model, xsum, minimize, INTEGER
import pandas as pd

model = Model("Diet")
table = r'table.csv'
df = pd.read_csv(table)

# Variables
X = [model.add_var(name=row['name'], var_type=INTEGER, lb=0, ub=row['max_serv']) for i, row in df.iterrows()]

#
# Constraints
#

# Energy
model += xsum(row['energy'] * X[i] for i, row in df.iterrows()) >= 1000 

# Protein
model += xsum(row['protein'] * X[i] for i, row in df.iterrows()) >= 55

# Calcium
model += xsum(row['calcium'] * X[i] for i, row in df.iterrows()) >= 800

model.objective = minimize(xsum(row['price'] * X[i] for i, row in df.iterrows()))

model.optimize()

print('Solution\tVar(x)')
print('-'*24)
for v in model.vars:
    print(f'{v.x}\t{v}')
