import numpy as np


chemicals = ['Acid', 'Caustic']
tanker_type = ['A', 'B', 'C', 'D']
demand_point = [1, 2, 3, 4, 5, 6, 7, '8_a', '8_b', 'b_c', 9, 10, 11, 12, 13]
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
    (9, 5, '8_a', 9),
    (9, 5, '8_b', 9),
]  # len = 17

# num of tankers: N[t]
N = [1, 5, 6, 0]

# length of routes(km): L[r]
L = [260, 450, 480, 340, 355, 370, 515, 550, 840, 770, 820, 435, 305]

# driving hours for each route: H[r]
H = [11, 13, 15, 13, 12, 12, 23, 24, 30, 26, 30, 13, 11, 13, 12, 13, 12]

# If route r contains demand point a: I[r][a]
I = [

]  # shape: (17, 11)

# In route r, if demand point a is in front of demand point b: J[r][a][b]
J = [

]  # shape: (17, 11, 11)

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
    [15, float('inf')],
]  # shape: (11, 2)

# Capacity for each tanker[t, k] for each chemical: C[t][k][m]
C = [
    [],
    [],
    [],
    [],
]  # shape: (4, N[t], 2)

# num of virtual tankers for tanker[t, k]
V = [

]  # shape: (4, N[t])

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
assert len(tanker_type) == len(N) == 4, (len(tanker_type), len(N))
assert len(route) == len(H) == len(L) == 17, (len(demand_point), len(H), len(route), len(L))
assert np.array(I).shape == (17, 11), np.array(I).shape
assert np.array(J).shape == (17, 11, 11), np.array(J).shape
assert np.array(W).shape == (11, 2), np.array(W).shape
assert len(C) == 4, len(C)
assert len(V) == 4, len(V)
assert np.array(D).shape == (11, 2), np.array(D).shape

print(f"{__name__} Shape Check Pass")
