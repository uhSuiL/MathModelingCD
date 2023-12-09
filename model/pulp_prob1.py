import pulp as pulp
import numpy as np


def solve(
        tanker_types:   list[int],
        route:          list[int],
        demand_point:   list[int],
        chemicals:      list[int],
        N,
        L,
        H,
        J,
        W,
        C,
        V,
        D,
):
    prob = pulp.LpProblem("myProblem", pulp.LpMinimize)

    # decision variables
    y = [
        [
            pulp.LpVariable(cat=pulp.LpBinary, name=f'y[{t}][{k}]')
            for k in range(N[t])
        ]
        for t in tanker_types
    ]  # shape: (len(tanker_types), len(range(N[t]))) -- y[t][k]
    
    print("y added")

    z = [
        [
            [
                [
                    pulp.LpVariable(cat=pulp.LpBinary, name=f'z[{t}][{k}][{n}][{r}]')
                    for r in route
                ]
                for n in range(V[t][k])
            ]
            for k in range(N[t])
        ]
        for t in tanker_types
    ]

    print("z added")

    x = [
        [
            [
                [
                    [
                        [
                            [
                                pulp.LpVariable(cat=pulp.LpInteger, lowBound=0, name=f'x[{t}][{k}][{n}][{r}][{a}][{b}][{m}]')
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

    print("x added")

    print("Decision Variables added")

    # objective
    prob += (
        1000 * sum([y[t][k]
                    for t in tanker_types for k in range(N[t])]) +
        0.36 * np.sum(np.array([z[t][k][n][r] * L[r]
                    for t in tanker_types for k in range(N[t]) for n in range(V[t][k]) for r in route]))
    )

    print("Objective added")

    # constraints
    for t in tanker_types:
        for k in range(N[t]):
            for n in chemicals:
                prob += np.sum(np.array([z[t][k][n][r] for r in route])) <= 1

    print("Constraint 1 added")

    for t in tanker_types:
        for k in range(N[t]):
            prob += np.sum(np.array([z[t][k][n][r] for r in route for n in range(V[t][k])])) <= y[t][k] * V[t][k]

    print("Constraint 2 added")

    for t in tanker_types:
        for k in range(N[t]):
            for r in route:
                for n in range(V[t][k]):
                    for a in demand_point:
                        for b in demand_point:
                            for m in chemicals:
                                prob += x[t][k][n][r][a][b][m] <= C[t][k][n] * z[t][k][n][r] * J[a][b]

    print("Constraint 3 added")

    for b in demand_point:
        for m in chemicals:
            prob += (
                np.sum(np.array([x[t][k][n][r][a][b][m]
                     for t in tanker_types for k in range(N[t]) for r in route for n in range(V[t][k]) for a in demand_point]))
                - np.sum(np.array([x[t][k][n][r][b][c][m]
                       for t in tanker_types for k in range(N[t]) for r in route for n in range(V[t][k]) for c in demand_point]))
                == D[b][m]
            )

    print("Constraint 4 added")

    for t in tanker_types:
        for k in range(N[t]):
            for r in route:
                for n in range(V[t][k]):
                    for b in demand_point:
                        for m in chemicals:
                            prob += (
                                sum([x[t][k][n][r][a][b][m] for a in demand_point])
                                - sum([x[t][k][n][r][b][c][m] for c in demand_point])
                                <= W[b][m]
                            )

    print("Constraint 5 added")

    for t in tanker_types:
        for k in range(N[t]):
            prob += np.sum(np.array([z[t][k][n][r] * H[r] for r in route for n in range(V[t][k])])) <= 5240

    print("Constraint 6 added")

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[status])
    return prob
