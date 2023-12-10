import pulp as pulp
import numpy as np
import pickle


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
    y = get_y(tanker_types, N, from_pkl=None)  # shape: (len(tanker_types), len(range(N[t]))) -- y[t][k]
    z = get_z(route, V, N, tanker_types, from_pkl=None)
    x = get_x(tanker_types, N, V, route, demand_point, chemicals, from_pkl=None)

    print("Decision Variables added")

    # objective
    prob += (
        1000 * sum([y[t][k]
                    for t in tanker_types for k in range(N[t])]) +
        0.36 * np.sum(np.array([z[t][k][n][r] * L[r]
                    for t in tanker_types for k in range(N[t]) for n in range(V[t][k]) for r in route]))
    )


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
                                prob += x[t][k][n][r][a][b][m] <= C[t][k][n] * z[t][k][n][r] * J[r][a][b]

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

    with open('./data/model.pkl', 'rb') as f:
        pickle.dump(prob, f)
    return prob


def get_y(tanker_types, N, from_pkl: str = None):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.loads(f)

    y = [
        [
            pulp.LpVariable(cat=pulp.LpBinary, name=f'y[{t}][{k}]')
            for k in range(N[t])
        ]
        for t in tanker_types
    ]  # shape: (len(tanker_types), len(range(N[t]))) -- y[t][k]

    with open("./data/y.pkl", 'wb') as f:
        pickle.dump(y, f)

    print("y computed")
    return y


def get_z(route, V, N, tanker_types, from_pkl: str = None):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.loads(f)

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

    with open("./data/z.pkl", 'wb') as f:
        pickle.dump(z, f)
    print("z computed")
    return z


def get_x(tanker_types, N, V, route, demand_point, chemicals, from_pkl: str = None):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.loads(f)

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

    with open("./data/x.pkl", 'wb') as f:
        pickle.dump(x, f)
    print("x computed")
    return x


def get_objective(tanker_types, route, y, N, z, L, V, from_pkl: str = None):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.loads(f)

    objective = (
            1000 * sum([y[t][k]
                        for t in tanker_types for k in range(N[t])]) +
            0.36 * np.sum(np.array([z[t][k][n][r] * L[r]
                                    for t in tanker_types for k in range(N[t]) for n in range(V[t][k]) for r in route]))
    )

    with open("./data/object.pkl", 'wb') as f:
        pickle.dump(objective, f)
    print("Objective computed")
    return objective


def get_constraint1(z, route, tanker_types, N, chemicals, from_pkl: str = None) -> list:
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.load(f)

    constraint1 = [
        np.sum(np.array([z[t][k][n][r] for r in route])) <= 1
        for t in tanker_types
        for k in range(N[t])
        for n in chemicals
    ]

    with open("./data/constraint1.pkl", 'wb') as f:
        pickle.dump(constraint1, f)
    return constraint1


def get_constraint2(tanker_types, N, z, route, y, V, from_pkl: str = "./data/constraint2.pkl"):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.load(f)

    constraint2 = [
        np.sum(np.array([z[t][k][n][r] for r in route for n in range(V[t][k])])) <= y[t][k] * V[t][k]
        for t in tanker_types
        for k in range(N[t])
    ]

    with open("./data/constraint2.pkl", 'wb') as f:
        pickle.dump(constraint2, f)
    return constraint2


def get_constraint3(tanker_types, N, route, demand_point, chemicals, x, C, z, J, V, from_pkl: str = None):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.load(f)

    constraint3 = [
        x[t][k][n][r][a][b][m] <= C[t][k][n] * z[t][k][n][r] * J[r][a][b]
        for t in tanker_types
        for k in range(N[t])
        for r in route
        for n in range(V[t][k])
        for a in demand_point
        for b in demand_point
        for m in chemicals
    ]

    with open("./data/constraint3.pkl", 'wb') as f:
        pickle.dump(constraint3, f)
    return constraint3


def get_constraint4(tanker_types, x, N, D, route, demand_point, chemicals, V, from_pkl: str = None):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.load(f)

    constraint4 = [
        np.sum(np.array([
            x[t][k][n][r][a][b][m]
            for t in tanker_types
            for k in range(N[t])
            for r in route
            for n in range(V[t][k])
            for a in demand_point
        ]))
        - np.sum(np.array([
            x[t][k][n][r][b][c][m]
            for t in tanker_types for k in range(N[t])
            for r in route for n in range(V[t][k])
            for c in demand_point
        ]))
        == D[b][m]

        for b in demand_point
        for m in chemicals
    ]

    with open("./data/constraint4.pkl", 'wb') as f:
        pickle.dump(constraint4, f)
    return constraint4


def get_constraint5(tanker_types, N, route, V, demand_point, chemicals, W, x, from_pkl: str = None):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.load(f)

    constraint5 = [
        np.sum(np.array([x[t][k][n][r][a][b][m] for a in demand_point]))
        - np.sum(np.array([x[t][k][n][r][b][c][m] for c in demand_point]))
        <= W[b][m]
        for t in tanker_types
        for k in range(N[t])
        for r in route
        for n in range(V[t][k])
        for b in demand_point
        for m in chemicals
    ]

    with open("./data/constraint5.pkl", 'wb') as f:
        pickle.dump(constraint5, f)
    return constraint5


def get_constraint6(tanker_types, N, z, H, route, V, from_pkl: str = None):
    if type(from_pkl) is str:
        with open(from_pkl, 'rb') as f:
            return pickle.load(f)
    constraint6 = [
        np.sum(np.array([z[t][k][n][r] * H[r] for r in route for n in range(V[t][k])])) <= 5240
        for t in tanker_types
        for k in range(N[t])
    ]

    with open("./data/constraint6.pkl", 'wb') as f:
        pickle.dump(constraint6, f)
    return constraint6
