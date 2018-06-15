from multiprocessing import Pool
import time
import os
import sys
import glob
import runMulti

def worker(path):
    runMulti.exe(path)

def makedir(dirName):
    if( os.path.exists(dirName) ):
    	pass
    else:
    	os.mkdir(dirName)

if __name__ == '__main__':
    start = time.time()

    target = sys.argv[1]
    print(target)

    makedir("fitting")
    makedir("initBG")

    margin = 2
    cpuNum = int( len(os.sched_getaffinity(0)) - margin )
    print("cpu:{0}".format(cpuNum))
    with Pool(cpuNum) as p:
        p.map(worker, glob.glob(target + "/*.csv"))

    elapsed_time = time.time() - start
    print ("elapsed_time:{:.4f}".format(elapsed_time) + "[sec]")
