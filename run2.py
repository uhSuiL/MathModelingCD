from model import prob2
from data.prob2 import *
from datetime import datetime


chemicals = list(range(len(chemicals)))
tanker_types = list(range(len(tanker_types)))
demand_points = list(range(len(demand_points)))
routes = list(range(len(routes)))

if __name__ == '__main__':
	now = datetime.now().strftime("%Y-%m-%d(%H-%M-%S)")

	prob2.solve(
		tanker_types,
		routes,
		demand_points,
		chemicals,
		N,
		L,
		H,
		J,
		W,
		C,
		D,
		info=now
	)
