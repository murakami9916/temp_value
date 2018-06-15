import sys
import numpy as np
import glob

#common = sys.argv[1] + "*.csv"
for (k, fname) in enumerate(glob.glob("*.csv")):
	f=np.loadtxt(fname,delimiter=",")

	f_x=np.array(f[:,0])
	f_y=np.array(f[:,1])

	x_new = f_x
	y_new = f_y

	x_renew=x_new[::-1]
	y_renew=y_new[::-1]

	data=np.array((x_renew,y_renew))
	data=data.transpose()

	name = "data_" + fname
	np.savetxt(name,data,fmt="%5f",delimiter=",")
