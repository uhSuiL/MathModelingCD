from data.prob1 import *
from model import pulp_prob1

if __name__ == '__main__':
    prob1_model = pulp_prob1.solve(
        list(range(len(tanker_types))),
        list(range(len(route))),
        list(range(len(demand_point))),
        chemicals,
        N,
        L,
        H,
        J,
        W,
        C,
        V,
        D,
    )
