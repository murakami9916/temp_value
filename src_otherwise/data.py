import glob
import numpy as np
import sys
import pandas as pd

def Union(path):

	#names = sorted( glob.glob("./" + path + "/*.csv") )
	names = sorted( glob.glob(path + "/*.csv") )
	c = 0

	for n in names:
		print(c, n, type(n))
		f = np.loadtxt(n, delimiter = ",")
		y = np.array(f[:,1])

		if(c == 0):
			union = y
		else:
			union = np.vstack((union, y))

		c = c + 1

	np.savetxt("output.csv", union.T, delimiter = ",", fmt = "%.5lf")

def Std(name):
	data = pd.read_csv(name, header=None)
	dmin = data.min().min()
	dmax = data.max().max()
	data = ( data - dmin ) / ( dmax - dmin )
	data.to_csv("output_std.csv", index=False, header=False)


if __name__ == '__main__':
	
	try:
		Union(sys.argv[1])
	except:
		print("error [Union]")
		sys.exit()

	try:
		Std()
	except:
		print("error [Std]")
		sys.exit()