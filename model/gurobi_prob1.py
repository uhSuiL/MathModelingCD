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
):
    model = gp.Model()

    # decision variables
    y = [
        [
            model.addVar(vtype=gp.GRB.BINARY, name=f'y[{t}][{k}]')
            for k in range(N[t])
        ]
        for t in tanker_types
    ]  # shape: (len(tanker_types), len(range(N[t]))) -- y[t][k]

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

    # objective
    model.setObjective(
        1000 * sum([y[t][k]
                    for t in tanker_types for k in range(N[t])]) +
        0.36 * sum([z[t][k][n][r] * L[r]
                    for t in tanker_types for k in range(N[t]) for n in range(V[t][k]) for r in route])
    )

    # constraints
    for t in tanker_types:
        for k in range(N[t]):
            for n in chemicals:
                model.addConstr(sum([z[t][k][n][r] for r in route]) <= 1, name="C1")

    for t in tanker_types:
        for k in range(N[t]):
            model.addConstr(sum([z[t][k][n][r] for r in route for n in range(V[t][k])]) <= y[t][k] * V[t][k], name="C2")

    for t in tanker_types:
        for k in range(N[t]):
            for r in route:
                for n in range(V[t][k]):
                    for a in demand_point:
                        for b in demand_point:
                            for m in chemicals:
                                model.addConstr(
                                    x[t][k][n][r][a][b][m] <= C[t][k][m] * z[t][k][n][r] * J[a][b],
                                    name="C3"
                                )

    for b in demand_point:
        for m in chemicals:
            model.addConstr(
                sum([x[t][k][n][r][a][b][m] for t in tanker_types for k in range(N[t]) for r in route for n in range(V[t][k]) for a in demand_point])
                - sum([x[t][k][n][r][b][c][m] for t in tanker_types for k in range(N[t]) for r in route for n in range(V[t][k]) for c in demand_point])
                == D[b][m],
                name="C4"
            )

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
                                name="C5"
                            )

    for t in tanker_types:
        for k in range(N[t]):
            model.addConstr(
                sum([z[t][k][n][r] * H[r] for r in route for n in range(V[t][k])]) <= 5240,
                name="C6"
            )

    model.update()
    model.optimize()
    return model, x, y, z
