from data.prob1 import *
from model import pulp_prob1
from datetime import datetime
from model import gurobi_prob1
import sys

sys.setrecursionlimit(10000)

tanker_types = list(range(len(tanker_types)))
route = list(range(len(route)))
demand_point = list(range(len(demand_point)))
chemicals = list(range(len(chemicals)))

if __name__ == '__main__':
	# prob1_model = pulp_prob1.solve(
	#     tanker_types,
	#     route,
	#     demand_point,
	#     chemicals,
	#     N,
	#     L,
	#     H,
	#     J,
	#     W,
	#     C,
	#     V,
	#     D,
	# )

	model, x, y = gurobi_prob1.solve(
		tanker_types,
		route,
		demand_point,
		chemicals,
		N,
		L,
		H,
		J,
		W,
		C,
		V,
		D,
		f'v_tk=700@{datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")}'
	)
