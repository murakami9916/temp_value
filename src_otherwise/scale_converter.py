import sys
import numpy as np

fname = sys.argv[1]

f=np.loadtxt(fname,delimiter=",")

f_x=np.array(f[:,0])
f_y=np.array(f[:,1])

x_new = f_x
y_new = f_y
#x_new = ( f_x - min(f_x) ) / ( max(f_x) - min(f_x) ) * 5
#y_new = ( f_y - min(f_y) ) / ( max(f_y) - min(f_y) ) * 6000 + 100

x_renew=x_new[::-1]
y_renew=y_new[::-1]

data=np.array((x_renew,y_renew))
data=data.transpose()

np.savetxt(fname,data,fmt="%5f",delimiter=",")
