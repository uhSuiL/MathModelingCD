import numpy as np


chemicals = ['Acid', 'Caustic']
tanker_types = ['A', 'B', 'C']
demand_points = [1, 2, 3, 4, 5, 6, 7, '8_a', '8_b', '8_c', 9]
routes = [
    (9, 5, 9),
    (9, 1, 9),
    (9, 1, 5, 9),
    (9, '8_a', 9),
    (9, '8_b', 9),
    (9, '8_c', 9),
    (9, 3, 9),
    (9, 3, 5, 9),
    (9, 2, 9),
    (9, 7, 9),
    (9, 7, 5, 9),
    (9, 4, 9),
    (9, 6, 9),
    (9, '8_a', 5, 9),
    (9, '8_b', 5, 9),
	(9, '8_c', 5, 9),
	(9, 5, '8_a', 9),
    (9, 5, '8_b', 9),
	(9, 5, '8_c', 9),
]  # len = 19

# num of tankers: N[k]
N = [1, 5, 6]

# length of routes(km): L[r]
L = [260, 450, 480, 340, 355, 370, 515, 550, 840, 770, 820, 435, 305, 340, 355, 370, 340, 355, 370]

# driving hours for each route: H[r]
H = [11, 13, 15, 13, 12, 12, 23, 24, 30, 26, 30, 13, 11, 13, 12, 12, 13, 12, 12]

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
    [15, 1e5],
    [15, 1e5],
    [15, 1e5],
    [6, 1e5],  # 5
    [15, 1e5],
    [15, 1e5],
    [15, 1e5],
    [6, 1e5],  # 8_b
    [15, 1e5],
    [15, 1e5],
]  # shape: (11, 2)

# Capacity for each type of tanker[k] for each chemical: C[k][m]
C = [
    [16, 0],
    [0, 16],
    [6, 16]
]  # shape: (3, 2)

# demand for each chemical of each demand point: D[a][m]
D = [
    [6000, 0],
    [2500, 0],
    [6000, 0],
    [1000, 0],
    [13000, 0],
    [5000, 0],
    [2000, 0],
    [4000, 0],
    [1000, 0],
    [2000, 0],
    [0, 60000],
]  # shape: (11, 2)

# =================== Shape Check ===================

assert len(chemicals) == 2, len(chemicals)
assert len(tanker_types) == len(N) == 3, (len(tanker_types), len(N))
assert len(demand_points) == 11, len(demand_points)
assert len(routes) == len(H) == len(L) == 19, (len(routes), len(H), len(L))
assert J.shape == (19, 11, 11), J.shape
assert np.array(W).shape == (11, 2), np.array(W).shape
assert len(C) == 3, len(C)
assert np.array(D).shape == (11, 2), np.array(D).shape

print(f"{__name__} Shape Check Pass")
