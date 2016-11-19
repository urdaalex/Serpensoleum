import json
import numpy as np


def matMult(arg):
	print(arg)
	a = np.matrix([1,2], [3,4])
	b = np.identity(3)

	res = a*b

	return json.dumps(res)

if __name__ == "__main__":
	res = matMult()
	return res


