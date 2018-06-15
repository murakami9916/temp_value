import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import datetime
import scipy as sp
from scipy import stats
import glob


if __name__ == '__main__':
	common = sys.argv[1] + "/para*"
	time = "\n\n" + str(datetime.datetime.today())
	for (k, ndir) in enumerate(glob.glob(common)):
		d = ndir + "/result*"
		std_gamma = []
		std_sigma = []
		std_base = []
		std_const = []
		mean_gamma = []
		mean_sigma = []
		mean_base = []
		mean_const = []
		for (k, mdir) in enumerate(glob.glob(d)):
			fname = mdir + "/para_trans1_0.DAT"
			dataFrame = pd.read_csv(fname, delim_whitespace=True, header = None)
			sigma = dataFrame.loc[:, 3]
			npsigma = np.array(sigma)
			gamma = dataFrame.loc[:, 4]
			npgamma = np.array(gamma)
			const = dataFrame.loc[:, 5]
			npconst = np.array(gamma)
			base = dataFrame.loc[:, 6]
			npbase = np.array(gamma)

			mean_sigma.append( np.mean(npsigma) )
			mean_gamma.append( np.mean(npgamma) )
			mean_const.append( np.mean(npconst) )
			mean_base.append( np.mean(npbase) )

			std_sigma.append( np.std(npsigma) )
			std_gamma.append( np.std(npgamma) )
			std_const.append( np.std(npconst) )
			std_base.append( np.std(npbase) )

			print(mdir)

		data = np.array((((((((mean_sigma, std_sigma, mean_gamma, std_gamma, mean_const, std_const, mean_base, std_base))))))))
		data=data.transpose()
		sf = ndir + "/statistics.csv"
		np.savetxt(sf, data, delimiter = ",", fmt = "%.7f")
		print("<OK!>\n")
