from data.prob1_opt import *
# from data.prob1_v2 import *
# from data.prob1_v3 import *
# from data.prob1_wy_ls import *
# from data.prob1_wy_ls_mini2 import *
# from model import pulp_prob1
from datetime import datetime
from model import gurobi_prob1
# from model import prob1_wy_ls
# from model import prob1_wy_ls2
import sys

sys.setrecursionlimit(10000)

tanker_types = list(range(len(tanker_types)))
route = list(range(len(route)))
demand_point = list(range(len(demand_point)))
chemicals = list(range(len(chemicals)))
# tanker_types = list(range(len(tanker_types)))
# routes = list(range(len(routes)))
# demand_points = list(range(len(demand_points)))
# chemicals = list(range(len(chemicals)))

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

	model, x, y, z = gurobi_prob1.solve(
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
		f'v_tk=800@{datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")}-v0'
	)

	# prob1_wy_ls2.solve(
	# 	tanker_types,
	# 	routes,
	# 	demand_points,
	# 	chemicals,
	# 	L,
	# 	D,
	# 	J,
	# 	C,
	# 	N,
	# 	W,
	# 	H,
	# 	info=datetime.now().strftime("%Y-%m-%d(%H-%M-%S)") + '@mini_v2'
	# )
