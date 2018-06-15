
import numpy as np
import matplotlib.pyplot as plt
import sys

def NMF(Y, R=2, n_iter=50000, init_H=[], init_U=[], verbose=False):

	eps = np.spacing(1)
	#正則項の重み
	l = 0.0001

	# size of input spectrogram
	M = Y.shape[0]
	print(M)
	N = Y.shape[1]
	print(N)
    
	# initialization
	if len(init_U):
		U = init_U
		R = init_U.shape[0]
	else:
		U = np.random.rand(R,N);
		#U = np.ones((R,N))

	if len(init_H):
		H = init_H;
		R = init_H.shape[1]
	else:
		H = np.random.rand(M,R)
		#H = np.loadtxt("ref.csv", delimiter = ",")

	oneH = np.ones(H.shape[1])
	oneU = np.ones(U.shape[1])
        
	# array to save the value of the euclid divergence
	cost = np.zeros(n_iter)

	# computation of Lambda (estimate of Y)
	Lambda = np.dot(H, U)

	# iterative computation
	s = np.zeros(n_iter)
	for i in range(n_iter):

		regH = l * np.dot(np.dot(oneH,H.T), np.dot(H,oneH.T))
		regU = l * np.dot(np.dot(oneU,U.T), np.dot(U,oneU.T))
		reg = regH + regU

		# compute euclid divergence
		cost[i] = euclid_divergence(Y, Lambda, reg)

		# update H
		H *= np.dot(Y, U.T) / (np.dot(np.dot(H, U), U.T) + regH + eps)
		#H *= np.dot(Y, U.T) / (np.dot(np.dot(H, U), U.T) + eps)

		# update U
		U *= np.dot(H.T, Y) / (np.dot(np.dot(H.T, H), U) + regU + eps)
		#U *= np.dot(H.T, Y) / (np.dot(np.dot(H.T, H), U) + eps)

		# recomputation of Lambda
		Lambda = np.dot(H, U)

	return [H, U, cost]

def euclid_divergence(Y, Yh, reg):
    d = 1 / 2 * (Y ** 2 + Yh ** 2 - 2 * Y * Yh).sum() + reg
    return d

if __name__ == '__main__':

	argc = len(sys.argv)
	if(argc<2):
		sys.exit()

	fname = sys.argv[1]
	np.random.seed(1)
	Y = np.loadtxt(fname, delimiter = ",")

	computed = NMF(Y, R=4)

	print('\ndecomposed\n---------------')
	print('H:\n', computed[0])
	print('U:\n', computed[1])
	print('HU:\n', np.dot(computed[0], computed[1]))
	print('cost:\n', computed[2])

	M = Y.shape[0]
	N = Y.shape[1]

	h = computed[0]
	u = computed[1]

	np.savetxt("H.csv", h, fmt="%.5f", delimiter = ",")
	np.savetxt("U.csv", u, fmt = "%.5f", delimiter = ",")
	np.savetxt("R.csv",  computed[2].T, fmt = "%.5f", delimiter = ",")

	fig = plt.figure("convergence")
	plt.plot(computed[2].T, marker = "o")
	plt.xlim(0,10)
	
	fig = plt.figure("weightFunc")
	plt.plot(range(N), computed[1].T, marker = "o")

	fig = plt.figure("baseFunc")
	plt.plot(range(M), computed[0])

	plt.show()