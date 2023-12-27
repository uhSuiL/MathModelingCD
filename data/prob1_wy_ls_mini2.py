import numpy as np


chemicals = ['Acid', 'Caustic']
tanker_types = ['A', 'B', 'C']
demand_points = [1, 5, 9]
routes = [
    (9, 5, 9),
    (9, 1, 9),
    (9, 1, 5, 9),
]  # len = 3

# num of tankers: N[k]
N = [1, 5, 6]

# length of routes(km): L[r]
L = [260, 450, 480]

# driving hours for each route: H[r]
H = [11, 13, 15]

def get_J(_route: list[tuple], _demand_point: list) -> np.array:
    J = np.zeros(shape=(len(_route), len(_demand_point), len(_demand_point)))
    for r_i in range(len(_route)):
        r = _route[r_i]
        for i in range(len(r) - 1):
            current_demand_point = r[i]
            next_demand_point = r[i + 1]
            current_demand_point_id = _demand_point.index(r[i])
            next_demand_point_id = _demand_point.index(r[i + 1])
            J[r_i][current_demand_point_id][next_demand_point_id] = 1
    return J


# In route r, if demand point a is in front of demand point b: J[r][a][b]
J = get_J(routes, demand_points)  # shape: (19, 11, 11)

# Weight limit for each type of chemical at each demand point: W[a][m]
W = [
    [15, 1e5],
    [6, 1e5],  # 5
    [15, 1e5],
]  # shape: (3, 2)

# Capacity for each type of tanker[k] for each chemical: C[k][m]
C = [
    [16, 0],
    [0, 16],
    [6, 16]
]  # shape: (3, 2)

# demand for each chemical of each demand point: D[a][m]
D = [
    [60, 0],
    [130, 0],
    [30, 5],
]  # shape: (3, 2)

# =================== Shape Check ===================

assert len(chemicals) == 2, len(chemicals)
assert len(tanker_types) == len(N) == 3, (len(tanker_types), len(N))
assert len(demand_points) == 3, len(demand_points)
assert len(routes) == len(H) == len(L) == 3, (len(routes), len(H), len(L))
assert J.shape == (3, 3, 3), J.shape
assert np.array(W).shape == (3, 2), np.array(W).shape
assert len(C) == 3, len(C)
assert np.array(D).shape == (3, 2), np.array(D).shape

print(f"{__name__} Shape Check Pass")
