import os
import numpy as np
import gurobipy as gp


def solve(
        tanker_types: list[int],
        routes: list[int],
        demand_points: list[int],
        chemicals: list[int],
        N: list[int],
        L: list[int],
        H: list[int],
        J: np.ndarray,
        W: np.ndarray,
        C: np.ndarray,
        D: np.ndarray,
        info: str
):  # 所有多维的应该全部转为ndarray
    if not os.path.exists(f'./output/prob2/{info}/'):
        os.makedirs(f'./output/prob2/{info}/')

    model = gp.Model()
    model.setParam(gp.GRB.Param.LogFile, f'./output/prob2/{info}/log.log')

    y1 = model.addVars([t for t in tanker_types], vtype=gp.GRB.INTEGER, lb=0, name='y1')
    y2 = model.addVars([t for t in tanker_types], vtype=gp.GRB.INTEGER, lb=0, name='y2')
    print("y1, y2 added")

    z = model.addVars([(t, r) for t in tanker_types for r in routes], vtype=gp.GRB.INTEGER, lb=0, name='z')
    print("z added")

    x = model.addVars([
        (t, r, a, b, m)
        for t in tanker_types
        for r in routes
        for a in demand_points
        for b in demand_points
        for m in chemicals
    ], vtype=gp.GRB.CONTINUOUS, lb=0, name='x')
    print("x added")

    model.setObjective(
        1000 * sum(N[t] + y1[t] + y2[t] for t in tanker_types)
        + 20000 * sum(y1[t] for t in tanker_types)
        - 10000 * sum(y2[t] for t in tanker_types)
        + 0.36 * sum(z[t, r] * L[r] for t in tanker_types for r in routes)
    )
    print("Objective set")

    model.addConstrs((
        sum(z[t, r] for t in tanker_types for r in routes) >= N[t] + y1[t] - y2[t]
        for t in tanker_types
    ), name="C1")
    print("Constraint 1 added")

    model.addConstrs((
        sum(x[t, r, a, b, m] for t in tanker_types for r in routes for a in demand_points)
        - sum(x[t, r, b, c, m] for t in tanker_types for r in routes for c in demand_points)
        == D[b, m]
        for b in demand_points
        for m in chemicals
    ), name="C2")
    print("Constraint 2 added")

    model.addConstrs((
        x[t, r, a, b, m] <= J[r, a, b] * C[t, m] * z[t, r]
        for t in tanker_types
        for r in routes
        for a in demand_points
        for b in demand_points
        for m in chemicals
    ), name="C3")
    print("Constraint 3 added")

    model.addConstrs((
        sum(x[t, r, a, b, m] for a in demand_points)
        - sum(x[t, r, b, c, m] for c in demand_points)
        <= z[t, r] * W[b, m]
        for t in tanker_types
        for r in routes
        for b in demand_points
        for m in chemicals
    ), name="C4")
    print("Constraint 4 added")

    model.addConstrs((
        sum(H[r] * z[t, r] for r in routes) <= 5240 * (N[t] + y1[t] - y2[t])
        for t in tanker_types
    ), name="C5")
    print("Constraint 5 added")

    model.optimize()

    print("\n========\n Finsh Solving \n========\n")
    write_model(f'./output/prob2/{info}/model[{info}]', model)
    return model, y1, y2, z, x


def write_model(path: str, model):
    suffix_list = ['mps', 'json', 'attr', 'sol', 'hnt']
    for suffix in suffix_list:
        try:
            model.write(path + '.' + suffix)
            print(suffix + ' written')
        except Exception as e:
            print(e)
    try:
        if model.status == 3:  # infeasible
            model.computeIIS()
            model.write(path + '.ilp')
    except Exception as e:
        print(e)
    print("files written")


def display_model(model):
    model.printStats()
    # model.display()
