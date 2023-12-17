import os
import gurobipy as gp


def solve(
        tanker_types: list[int],
        routes: list[int],
        demand_points: list[int],
        chemicals: list[int],
        L,
        D,
        J,
        C,
        N,
        W,
        H,
        info: str
):
    if not os.path.exists(f'./output/{__name__}/{info}/'):
        os.makedirs(f'./output/{__name__}/{info}/')

    model = gp.Model()
    model.setParam(gp.GRB.Param.LogFile, f'./output/{__name__}/{info}/log.log')

    print("=================== Adding Decision Variables ===================")

    x = model.addVars((
        (k, r)
        for k in tanker_types
        for r in routes
    ), lb=0, vtype=gp.GRB.INTEGER, name='x')
    print("x added")

    y = model.addVars((
        (m, a, b)
        for m in chemicals
        for a in demand_points
        for b in demand_points
    ), lb=0, vtype=gp.GRB.CONTINUOUS, name='y')
    print("y added")

    print("=================== Decision Variables Added ===================")
    print("======================= Setting Objective =======================")

    model.setObjective(
        1000 * sum(x[k, r] for k in tanker_types for r in routes)
        + 0.36 * sum(L[r] * x[k, r] for k in tanker_types for r in routes)
    )

    print("========================= Objective Set =========================")
    print("======================= Adding Constraints =======================")

    model.addConstrs((
        sum(x[k, r] for r in routes) <= N[k]
        for k in tanker_types
    ), name='C0')
    print("C0 added")

    model.addConstrs((
        sum(y[m, a, b] * J[r][a][b] for r in routes for a in demand_points)
        - sum(y[m, b, c] * J[r][b][c] for r in routes for c in demand_points)
        == D[b][m]
        for b in demand_points
        for m in chemicals
    ), name='C1')
    print("C1 added")

    model.addConstrs((
        y[m, a, b] * J[r][a][b] <= sum(C[k][m] * x[k, r] for k in tanker_types)
        for m in chemicals
        for a in demand_points
        for b in demand_points
        for r in routes
    ), name='C2')
    print("C2 added")

    model.addConstrs((
        sum(x[k, r] * H[r] for r in routes) <= 5240 * N[k]
        for k in tanker_types
    ), name='C3')
    print("C3 added")

    model.addConstrs((
        sum(y[m, a, b] * J[r][a][b] for m in chemicals) <= 16 * sum(x[k, r] for k in tanker_types)
        for a in demand_points
        for b in demand_points
        for r in routes
    ), name='C4')
    print("C4 added")

    model.addConstrs((
        y[m, a, b] * J[r][a][b] - y[m, b, c] * J[r][b][c] <= W[b][m] * sum(x[k, r] for k in tanker_types)
        for a in demand_points
        for b in demand_points
        for c in demand_points
        for r in routes
        for m in chemicals
    ), name='C5')
    print("C5 added")

    print("========================== Constraints added ==========================")

    model.optimize()

    write_model(f'./output/{__name__}/{info}/{__name__}[{info}]', model)


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
