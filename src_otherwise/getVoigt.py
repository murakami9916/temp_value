import numpy as np
import sys

def voigtFunc(x, c, a, w, l):
	gauss = pow(2.0, -pow((x - c) / w, 2))
	lorentz = 1.0 / (1.0 + pow((x - c) / w, 2))
	voigt = a * ( (1-l) * gauss + l * lorentz )
	return voigt

if __name__ == '__main__':
	argc = len(sys.argv)
	if(argc < 3):
		print("There are not enough arguments")
		sys.exit()
	fname = sys.argv[1]
	raw = sys.argv[2]
	para = np.loadtxt(fname, delimiter=",")
	f = np.loadtxt(raw, delimiter=",")
	f_x = f[:,0]
	f_y = f[:,1]
	bg  = f[:,2]
	print(para)
	
	for p in range(len(para)):
		y_temp = []
		for i in range(len(f)):
			x = f[i,0]
			a = para[p, 0]
			c = para[p, 1]
			w = para[p, 2] / 2.0
			l = para[p, 3]
			y_temp.append(voigtFunc(x, c, a, w, l) + bg[i])

		y_array = np.array(y_temp)

		if(p == 0):
			y = y_array
			fit = y_array
		else:
			y = np.vstack((y, y_array))
			print(p, end = "")
			print(type(y_array))
			print(len(y_array))
			fit = fit + y_array

	fit = fit - len(para) * bg + bg

	y = np.vstack((bg, y))
	y = np.vstack((fit, y))
	y = np.vstack((f_y, y))
	y = np.vstack((f_x, y))

	y = y.transpose()
	np.savetxt("y.csv", y, fmt="%5f",delimiter=",")