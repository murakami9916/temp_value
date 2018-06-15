import subprocess
import os
import sys
import csv
import shutil
import glob
import matplotlib.pyplot as plt
import numpy as np

def plot(name, t):

	f = np.loadtxt("out_background.csv", delimiter = ",", skiprows = 1)
	x = np.array(f[:,0])
	x = x[::-1]
	sp = np.array(f[:,1])
	sp = sp[::-1]
	bg = np.array(f[:,2])
	bg = bg[::-1]

	plt.clf()
	plt.figure(fname)
	plt.scatter(x,sp, edgecolors="red", c = "#FFFFFF")
	plt.plot(x,bg)
	plt.xlim(plt.xlim()[::-1])
	plt.title(t+"_"+fname)
	plt.xlabel('Binding Energy[eV]')
	plt.ylabel('Intensity [a.u.]')
	
	plt.savefig(fname + "_" + t)

	#plt.show()

def exe(path, fname, cmd, t):
	print(path)
	subprocess.run([cmd, path])

	plot(fname, t)

	if( os.path.exists(fname + "_" + t) ):
		pass
	else:
		os.mkdir(fname + "_" + t)

	for file in glob.glob("*.csv"):
		shutil.move(file, fname + "_" + t + "/" + os.path.basename(file))

	print("*********************\n")
	print("[" + fname + "]")
	print("*********************\n")

if __name__ == '__main__':
	target = sys.argv[1]
	print(target)

	error = []
	for path in glob.glob(target + "/*.csv"):
		fname, ext = os.path.splitext( os.path.basename(path) )
		print(fname)

		try:
			exe(path, fname, "ActiveShirley.exe", "point")

		except:
			error.append(fname)

	print("*********************")
	print("*****  Finish  ******")
	print("*********************")

	with open('list.csv', 'w') as f:
	    writer = csv.writer(f, lineterminator='\n')
	    writer.writerow(error)