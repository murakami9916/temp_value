import numpy as np
import sys
import os

def func(names):
	f1 = np.array( np.loadtxt(names[0], delimiter = ",") )
	f2 = np.array( np.loadtxt(names[1], delimiter = ",") )

	for i in range(1,10):
		if( "union" in locals() ):
			print( "[%d] %d:%d" %(i ,i, (10-i)) )
			y = f1 * i * 0.1 + f2 * (10-i) * 0.1
			union = np.vstack((union, y))
		else:
			print( "[%d] %d:%d" %(i ,i, (10-i)) )
			union = f1 * i * 0.1 + f2 * (10-i) * 0.1

	np.savetxt("output.csv", union.T, delimiter = ",", fmt = "%.5lf")

if __name__ == '__main__':
	if(len(sys.argv) < 3):
		sys.exit()

	names = [ sys.argv[1], sys.argv[2] ]
	print("INPUT:%s" %(names))
	func(names)