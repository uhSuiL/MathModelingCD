import os

import gurobipy as gp


def solve(
        tanker_types:   list[int],
        route:          list[int],
        demand_point:   list[int],
        chemicals:      list[int],
        N,
        L,
        H,
        # I,
        J,
        W,
        C,
        V,
        D,
        info
):
    if not os.path.exists(f'./output/prob1/{info}/'):
        os.makedirs(f'./output/prob1/{info}/')

    model = gp.Model()
    model.setParam(gp.GRB.Param.LogFile, f'./output/prob1/{info}/log.log')

    # decision variables
    # shape: (len(tanker_types), len(range(N[t]))) -- y[t][k]
    y = model.addVars([(t, k) for t in tanker_types for k in range(N[t])], vtype=gp.GRB.BINARY, name="y")
    print("y added")

    z = model.addVars([
        (t, k, n, r)
        for t in tanker_types
        for k in range(N[t])
        for n in range(V[t][k])
        for r in route
    ], vtype=gp.GRB.BINARY, name='z')
    print("z added")

    x = model.addVars([
        (t, k, n, r, a, b, m)
        for t in tanker_types
        for k in range(N[t])
        for n in range(V[t][k])
        for r in route
        for a in demand_point
        for b in demand_point
        for m in chemicals
    ], vtype=gp.GRB.CONTINUOUS, lb=0, name='x')
    print("x added")

    model.update()
    print("decision variables added")

    # objective

    model.setObjective(
        1000 * sum([
            y[t, k]
            for t in tanker_types
            for k in range(N[t])
        ]) +
        0.36 * sum([
            z[t, k, n, r] * L[r]
            for t in tanker_types
            for k in range(N[t])
            for n in range(V[t][k])
            for r in route
        ])
    )
    print("objective added")

    # constraints

    model.addConstrs((
        sum([z[t, k, n, r] for r in route]) <= 1
        for t in tanker_types
        for k in range(N[t])
        for n in range(V[t][k])
    ), name="C1")
    print("constraint1 added")

    model.addConstrs((
        sum([z[t, k, n, r] for r in route for n in range(V[t][k])]) - y[t, k] * V[t][k] <= 0
        for t in tanker_types
        for k in range(N[t])
    ), name="C2")
    print("constraint2 added")

    model.addConstrs((
        x[t, k, n, r, a, b, m] - C[t][k][m] * z[t, k, n, r] * J[r][a][b] <= 0
        for t in tanker_types
        for k in range(N[t])
        for r in route
        for n in range(V[t][k])
        for a in demand_point
        for b in demand_point
        for m in chemicals
    ), name="C3")
    print("constraint3 added")

    model.addConstrs((
        sum([
            x[t, k, n, r, a, b, m]
            for t in tanker_types
            for k in range(N[t])
            for r in route
            for n in range(V[t][k])
            for a in demand_point
        ])
        - sum([
            x[t, k, n, r, b, c, m]
            for t in tanker_types
            for k in range(N[t])
            for r in route
            for n in range(V[t][k])
            for c in demand_point]
        )
        >= D[b][m]

        for b in demand_point
        for m in chemicals
    ), name="C4")
    print("constraint4 added")

    model.addConstrs((
        sum([x[t, k, n, r, a, b, m] for a in demand_point])
        - sum([x[t, k, n, r, b, c, m] for c in demand_point])
        <= W[b][m]
        for t in tanker_types
        for k in range(N[t])
        for r in route
        for n in range(V[t][k])
        for b in demand_point
        for m in chemicals
    ), name="C5")
    print("Constraint 5 added")

    model.addConstrs((
        sum([z[t, k, n, r] * H[r] for r in route for n in range(V[t][k])]) <= 5240
        for t in tanker_types
        for k in range(N[t])
    ), name="C6")
    print("Constraint 6 added")

    print("constraints added")

    model.update()
    model.optimize()
    print("finish solving")

    write_model(f'./output/prob1/{info}/gurobi_model[{info}]', model)
    display_model(model)
    return model, x, y, z


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
