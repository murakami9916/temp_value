import numpy as np
import matplotlib.pyplot as plt
import sys

def reproduct(k=2):
	base = np.loadtxt("H.csv", delimiter = ",")
	org = np.loadtxt("org.csv", delimiter = ",")
	weight = np.loadtxt("U.csv", delimiter = ",")

	for i in range(org.shape[1]):
		y = range( org.shape[0] )
		fit = np.zeros( org.shape[0] )

		for j in range(k):
			y_temp =  base[:,j] * weight[j,i]
			y = np.vstack((y, y_temp))
			fit = fit + y_temp

		plt.clf()
		plt.title("Number. %d" %i)
		plt.scatter(range(org.shape[0]),org[:,i], c = "r", marker="o", s = 20, label="org")
		plt.plot(range(org.shape[0]),fit, c = "b",label="fit")
		for j in range(k):
			plt.plot(range(org.shape[0]),y[j+1])

		plt.legend()
		
		fname = "number" + str(i)
		plt.savefig(fname)

if __name__ == '__main__':
	reproduct()