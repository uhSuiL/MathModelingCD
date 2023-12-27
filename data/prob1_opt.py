import numpy as np


chemicals = ['Acid', 'Caustic']
tanker_types = ['A', 'B', 'C', 'D']
demand_point = [1, 2, 3, 4, 5, 6, 7, '8_a', '8_b', '8_c', 9]
route = [
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

# num of tankers: N[t]
N = [1, 2, 6, 5]

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
J = get_J(route, demand_point)  # shape: (17, 11, 11)

# Weight limit for each type of chemical at each demand point: W[a][m]
W = [
    [15, float('inf')],
    [15, float('inf')],
    [15, float('inf')],
    [15, float('inf')],
    [6, float('inf')],  # 5
    [15, float('inf')],
    [15, float('inf')],
    [15, float('inf')],
    [6, float('inf')],  # 8_b
    [15, float('inf')],
    [15, float('inf')],
]  # shape: (11, 2)

# Capacity for each tanker[t, k] for each chemical: C[t][k][m]
C = [
    [(16, 0) for j in range(N[0])],
    [(0, 16) for j in range(N[1])],
    [(6, 16) for j in range(N[2])],
    [(16, 6) for j in range(N[3])],
]  # shape: (4, N[t], 2)

# num of virtual tankers for tanker[t, k]
V = [
    [800] * N[0],
    [800] * N[1],
    [800] * N[2],
    [800] * N[3],
]  # shape: (4, N[t])

# demand for each chemical of each demand point: D[a][m]
D = np.array([
    [6000, 0],
    [2500, 0],
    [6000, 0],
    [1000, 0],
    [13000, 0],  # start for caustic
    [5000, 0],
    [2000, 0],
    [4000, 0],
    [1000, 0],
    [2000, 0],
    [0, 60000],  # start for acidic
])  # shape: (11, 2)

D[4, 1] = - np.sum(D[:, 1])
D[10, 0] = - np.sum(D[:, 0])


# =================== Shape Check ===================

assert len(chemicals) == 2, len(chemicals)
assert len(tanker_types) == len(N) == 4, (len(tanker_types), len(N))
assert len(demand_point) == 11, len(demand_point)
assert len(route) == len(H) == len(L) == 19, (len(route), len(H), len(L))
# assert np.array(I).shape == (17, 11), np.array(I).shape
assert J.shape == (19, 11, 11), J.shape
assert np.array(W).shape == (11, 2), np.array(W).shape
assert len(C) == 4, len(C)
assert len(V) == 4, len(V)
assert D.shape == (11, 2), D.shape

print(f"{__name__} Shape Check Pass")
