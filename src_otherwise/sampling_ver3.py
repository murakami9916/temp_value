import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import datetime
import scipy as sp
from scipy import stats

time = "\n\n" + str(datetime.datetime.today())

argc = len(sys.argv)
if(argc < 4):
	print("There are not enough arguments")
	sys.exit()

fname = sys.argv[1]
peakNum = sys.argv[2]
peakNum = int(peakNum)
info = sys.argv[3]
para = 4 #org 4
flag = 0

if(info == 'mu'):
	getNum = 1
	figname = 'The posterior distribution of position'
	xaxis = 'position [eV]'
	fig = 'sampling_mu'
elif(info == 'h'):
	getNum = 2
	figname = 'The posterior distribution of area'
	xaxis = 'area [a.u.]'
	fig = 'sampling_area'
elif(info == 'w'):
	getNum = 3
	figname = 'The posterior distribution of gauss width'
	xaxis = 'gauss width [eV]'
	fig = 'sampling_gaussWidth'
elif(info == 'l'):
	getNum = 4
	figname = 'The posterior distribution of Lorentz width'
	xaxis = 'gauss width [eV]'
	fig = 'sampling_LorentzWidth'
elif(info == 'c'):
	getNum = para * peakNum + 1
	figname = 'The posterior distribution of BackgroundConst'
	xaxis = 'BackgroundConst'
	flag = 1
	fig = 'sampling_BackgroundConst'
elif(info == 'b'):
	getNum = para * peakNum + 2
	figname = 'The posterior distribution of Base'
	xaxis = 'Base'
	flag = 1
	fig = 'sampling_Base'
elif(info == 'e'):
	getNum = 0
	figname = 'The posterior distribution of E'
	xaxis = 'ErrorFunction'
	flag = 1
	fig = 'sampling_ErrorFunction'
else:
	print("Argument is incorrect")
	sys.exit()

dataFrame = pd.read_csv(fname, delim_whitespace=True, header = None)

if(flag == 1):
	data = dataFrame.loc[:, getNum]
	npdata = np.array(data)

	sampling = "sampling:" + str( np.size(npdata) ) + "\n\n"

	print("mean is %.2f" %np.mean(npdata))
	mean = "mean of " + info + "\n" + str(round(np.mean(npdata),3)) + "\n"
	print("var is %.2f" %np.var(npdata))
	var = "var of " + info + "\n" + str(round(np.var(npdata),6)) + "\n"
	print("median is %.2f" %np.median(npdata))
	median = "median of " + info + "\n" + str(round(np.median(npdata),3)) + "\n"
	print("\nmin:%.3f\nmax:%.3f" %( np.min(npdata), np.max(npdata) ))

	statistics = "statistics of " + info + "\n" + sampling + mean + "\n" + var + "\n" + median + time

	out = "statistics_" + info + ".txt"
	f = open(out,'w')
	f.write(statistics)
	f.close()

	n = np.size(npdata)
	sturges = int( 1 + np.log2(n) )
	sturges = 100


	plt.figure(fig ,figsize = (9, 6))
	plt.title(figname, fontsize=32, fontname='Times New Roman')
	plt.xlabel(xaxis, fontsize=24, fontname='Times New Roman')
	plt.ylabel("frequency[time]", fontsize=24, fontname='Times New Roman')
	plt.tick_params(labelsize = 15)
	plt.rcParams['xtick.direction'] = 'in'
	plt.rcParams['ytick.direction'] = 'in'

	#plt.hist(npdata, bins = sturges, alpha = 0.4, range = (np.min(npdata), np.max(npdata)) )
	plt.hist(npdata, bins = sturges, alpha = 0.4, range = ( 0, 0.06 ) )
	plt.show()
	sys.exit()

getline = np.array(range(getNum, para*peakNum + 1, 4))
data = dataFrame.loc[:, getline]
npdata = np.array(data)

sampling = "sampling:" + str( np.size(npdata) / peakNum ) + "\n\n"

mean = "mean of " + info + "\n"
print("mean is")
for num in range(peakNum):
	print("[%d] %.2f" %( num, np.mean(npdata[:,num]) ))
	mean = mean + "[" + str(num) + "] " + str(round(np.mean(npdata[:,num]),3)) + "\n"

var = "var of " + info + "\n"
print("\nvar is")
for num in range(peakNum):
	print("[%d] %.6f" %( num, np.var(npdata[:,num]) ))
	var = var + "[" + str(num) + "] " + str(round(np.var(npdata[:,num]),6)) + "\n"

median = "median of " + info + "\n"
print("\nmedian is")
for num in range(peakNum):
	print("[%d] %.3f" %( num, np.median(npdata[:,num]) ))
	median = median + "[" + str(num) + "] " + str(round(np.median(npdata[:,num]),3)) + "\n"

print("\nmin:%.3f\nmax:%.3f" %( np.min(npdata), np.max(npdata) ))

statistics = "statistics of " + info + "\n" + sampling + mean + "\n" + var + "\n" + median + time

out = "statistics_" + info + ".txt"
f = open(out,'w')
f.write(statistics)
f.close()

n = np.size(npdata) * peakNum
#sturges = int( 1 + np.log2(n) )
sturges = 100

plt.figure(fig ,figsize = (9, 6))
plt.title(figname, fontsize=32, fontname='Times New Roman')
plt.xlabel(xaxis, fontsize=24, fontname='Times New Roman')
plt.ylabel("frequency[time]", fontsize=24, fontname='Times New Roman')
plt.tick_params(labelsize = 15)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

for i in range(peakNum):
	l = "peak[" + str(i) + "]"
	#plt.hist(npdata[:,i],label = l ,bins = sturges, alpha = 0.4, range = ( np.min(npdata), np.max(npdata)) )
	plt.hist(npdata[:,i],label = l ,bins = sturges, alpha = 0.4, range = ( 0.0, 0.3 ))
	plt.legend(fontsize=18)

plt.show()