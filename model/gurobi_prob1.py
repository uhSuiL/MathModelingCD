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
    model = gp.Model()
    if not os.path.exists(f'./output/{info}/'):
        os.mkdir(f'./output/{info}/')
    # decision variables
    y = [
        [
            model.addVar(vtype=gp.GRB.BINARY, name=f'y[{t}][{k}]')
            for k in range(N[t])
        ]
        for t in tanker_types
    ]  # shape: (len(tanker_types), len(range(N[t]))) -- y[t][k]
    # y = model.addVars([(t, k) for t in tanker_types for k in range(N[t])], vtype=gp.GRB.BINARY, name="y")

    z = [
        [
            [
                [
                    model.addVar(vtype=gp.GRB.BINARY, name=f'z[{t}][{k}][{n}][{r}]')
                    for r in route
                ]
                for n in range(V[t][k])
            ]
            for k in range(N[t])
        ]
        for t in tanker_types
    ]
    # z = model.addVars([
    #     (t, k, n, r)
    #     for t in tanker_types
    #     for k in range(N[t])
    #     for n in range(V[t][k])
    #     for r in route
    # ], vtype=gp.GRB.BINARY, name='z')

    x = [
        [
            [
                [
                    [
                        [
                            [
                                model.addVar(vtype=gp.GRB.INTEGER, lb=0, name=f'x[{t}][{k}][{n}][{r}][{a}][{b}][{m}]')
                                for m in chemicals
                            ]
                            for b in demand_point
                        ]
                        for a in demand_point
                    ]
                    for r in route
                ]
                for n in range(V[t][k])
            ]
            for k in range(N[t])
        ]
        for t in tanker_types
    ]
    # x = model.addVars([
    #     (t, k, n, r, a, b, m)
    #     for t in tanker_types
    #     for k in range(N[t])
    #     for n in range(V[t][k])
    #     for r in route
    #     for a in demand_point
    #     for b in demand_point
    #     for m in chemicals
    # ], vtype=gp.GRB.INTEGER, lb=0, name='x')

    model.update()
    print("decision variables added")

    # objective
    model.setObjective(
        1000 * sum([y[t][k]
                    for t in tanker_types for k in range(N[t])]) +
        0.36 * sum([z[t][k][n][r] * L[r]
                    for t in tanker_types for k in range(N[t]) for n in range(V[t][k]) for r in route])
    )

    # model.setObjective(
    #     1000 * sum([
    #         y[t, k]
    #         for t in tanker_types
    #         for k in range(N[t])
    #     ]) +
    #     0.36 * sum([
    #         z[t, k, n, r] * L[r]
    #         for t in tanker_types
    #         for k in range(N[t])
    #         for n in range(V[t][k])
    #         for r in route
    #     ])
    # )
    print("objective added")

    # constraints
    for t in tanker_types:
        for k in range(N[t]):
            for n in range(V[t][k]):
                model.addConstr(sum([z[t][k][n][r] for r in route]) <= 1)

    # model.addConstrs([
    #     sum([z[t, k, n, r] for r in route]) <= 1
    #     for t in tanker_types
    #     for k in range(N[t])
    #     for n in range(V[t][k])
    # ], name="C1")
    print("constraint1 added")

    for t in tanker_types:
        for k in range(N[t]):
            model.addConstr(sum([z[t][k][n][r] for r in route for n in range(V[t][k])]) <= y[t][k] * V[t][k])

    # model.addConstrs([
    #     sum([z[t, k, n, r] for r in route for n in range(V[t][k])]) <= y[t, k] * V[t][k]
    #     for t in tanker_types
    #     for k in range(N[t])
    # ], name="C2")
    print("constraint2 added")

    for t in tanker_types:
        for k in range(N[t]):
            for r in route:
                for n in range(V[t][k]):
                    for a in demand_point:
                        for b in demand_point:
                            for m in chemicals:
                                model.addConstr(
                                    x[t][k][n][r][a][b][m] <= C[t][k][m] * z[t][k][n][r] * J[r][a][b],
                                )

    # model.addConstrs([
    #     x[t, k, n, r, a, b, m] <= C[t][k][m] * z[t, k, n, r] * J[r][a][b]
    #     for t in tanker_types
    #     for k in range(N[t])
    #     for r in route
    #     for n in range(V[t][k])
    #     for a in demand_point
    #     for b in demand_point
    #     for m in chemicals
    # ], name="C3")
    print("constraint3 added")

    for b in demand_point:
        for m in chemicals:
            model.addConstr(
                sum([x[t][k][n][r][a][b][m] for t in tanker_types for k in range(N[t]) for r in route for n in range(V[t][k]) for a in demand_point])
                - sum([x[t][k][n][r][b][c][m] for t in tanker_types for k in range(N[t]) for r in route for n in range(V[t][k]) for c in demand_point])
                == D[b][m],
            )

    # model.addConstrs([
    #     sum([
    #         x[t, k, n, r, a, b, m]
    #         for t in tanker_types
    #         for k in range(N[t])
    #         for r in route
    #         for n in range(V[t][k])
    #         for a in demand_point
    #     ])
    #     - sum([
    #         x[t, k, n, r, b, c, m]
    #         for t in tanker_types
    #         for k in range(N[t])
    #         for r in route
    #         for n in range(V[t][k])
    #         for c in demand_point]
    #     )
    #     == D[b][m]
    #
    #     for b in demand_point
    #     for m in chemicals
    # ], name="C4")
    print("constraint4 added")

    for t in tanker_types:
        for k in range(N[t]):
            for r in route:
                for n in range(V[t][k]):
                    for b in demand_point:
                        for m in chemicals:
                            model.addConstr(
                                sum([x[t][k][n][r][a][b][m] for a in demand_point])
                                - sum([x[t][k][n][r][b][c][m] for c in demand_point])
                                <= W[b][m],
                            )

    # model.addConstrs([
    #     sum([x[t, k, n, r, a, b, m] for a in demand_point])
    #     - sum([x[t, k, n, r, b, c, m] for c in demand_point])
    #     <= W[b][m]
    #     for t in tanker_types
    #     for k in range(N[t])
    #     for r in route
    #     for n in range(V[t][k])
    #     for b in demand_point
    #     for m in chemicals
    # ], name="C5")
    print("Constraint 5 added")

    for t in tanker_types:
        for k in range(N[t]):
            model.addConstr(
                sum([z[t][k][n][r] * H[r] for r in route for n in range(V[t][k])]) <= 5240,
            )

    # model.addConstrs([
    #     sum([z[t, k, n, r] * H[r] for r in route for n in range(V[t][k])]) <= 5240
    #     for t in tanker_types
    #     for k in range(N[t])
    # ], name="C6")
    print("Constraint 6 added")

    print("constraints added")

    model.update()
    model.optimize()
    print("finish solving")


    model.write(f'./output/{info}/gurobi_model[{info}].mps')
    model.write(f'./output/{info}/gurobi_model[{info}].json')
    model.write(f'./output/{info}/gurobi_model[{info}].ilp')
    print("files written")
    return model, x, y, z
