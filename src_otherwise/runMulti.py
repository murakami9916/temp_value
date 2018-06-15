import subprocess
import os
import sys
import csv
import shutil
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot(name):
	f = np.loadtxt("out_background.csv", delimiter = ",", skiprows = 1)
	x = np.array(f[:,0])
	x = x[::-1]
	sp = np.array(f[:,1])
	sp = sp[::-1]
	bg = np.array(f[:,2])
	bg = bg[::-1]

	plt.clf()
	plt.figure(name)
	plt.plot(x,sp)
	plt.plot(x,bg)
	plt.xlim(plt.xlim()[::-1])
	plt.title(name)
	plt.xlabel('Binding Energy[eV]')
	plt.ylabel('Intensity [a.u.]')

	plt.savefig(name+"_initBG")

	#plt.show()

def bestFitting(name):

	resname = "result_peak_search.csv"
	print(resname)
	f = pd.read_csv(resname,index_col=0)

	plt.clf()
	plt.rcParams['xtick.direction'] = 'in'
	plt.rcParams['ytick.direction'] = 'in'
	fig = plt.figure(name ,figsize=(8, 6), dpi=80)
	spectrum = f["spectrum"]

	num_col = f.shape[1]
	print(num_col)


	plt.plot(spectrum, color="red", label="spectrum")

	for k in range(5, num_col+1, 1):
		n = "peak[" + str(k-5) + "]"
		print(n)
		peak = f[n]
		plt.plot(peak, label="peak[%d]" %(k-5))

	background = f["background"]
	plt.plot(background, label="background")
	fitting = f["fitting"]
	plt.plot(fitting, color="blue", linewidth=2, label="fitting")

	#plt.scatter(spectrum, s=50, c="#FFFFFF", linewidths=1, alpha=0.7, edgecolors="red", label="spectrum")

	plt.title(name)
	plt.xlabel("BindingEnergy [eV]",fontname="serif", fontsize=12)
	plt.ylabel("Intensity [a.u.]",fontname="serif", fontsize=12)
	plt.gca().invert_xaxis()

	plt.savefig(name + "_fitting")
	return 0

def exe(path):
	fname, ext = os.path.splitext( os.path.basename(path) )

	if( os.path.exists(fname) ):
		pass
	else:
		os.mkdir(fname)

	os.chdir(fname)

	print(path)
	rePath = "../" + path
	#subprocess.run(["ActiveShirley", rePath])
	logTxt = open('log.txt', 'w')
	subprocess.call(["ActiveShirley", rePath], stdout=logTxt, stderr=logTxt)

	plot(fname)
	bestFitting(fname)

	shutil.copy(fname+"_initBG.png", "../initBG")
	shutil.copy(fname+"_fitting.png", "../fitting")

	os.chdir("../")

	print("*********************\n")
	print("[" + fname + "]")
	print("*********************\n")

if __name__ == '__main__':
	target = sys.argv[1]
	print(target)

	if( os.path.exists("fitting") ):
		pass
	else:
		os.mkdir("fitting")

	if( os.path.exists("initBG") ):
		pass
	else:
		os.mkdir("initBG")

	error = []
	for path in glob.glob(target + "/*.csv"):
		#try:
		#	exe(path, fname, "ActiveShirley.exe", "point")
		#except:
		#	error.append(fname)
		exe(path)

	print("*********************")
	print("*****  Finish  ******")
	print("*********************")

	with open('list.csv', 'w') as f:
	    writer = csv.writer(f, lineterminator='\n')
	    writer.writerow(error)
