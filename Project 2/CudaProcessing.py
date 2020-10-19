import numpy as np
import cupy as cp
from timeit import default_timer as timer    

#I'm running on cupy-cuda11.0 
#Please also install CUDA toolkit, in order to execute cupy python library
#My is running on 

def ReadFile():
    edge = np.loadtxt("roadNet-PA.txt", dtype="int32", skiprows=4)
    array = np.array(edge)
    return array

def FullAdjMatrix(arr1):
    size = cp.unique(arr1).size
    cpSortedArr = arr1[arr1[:,0].argsort()]

    arr = cp.zeros(size, dtype="int32")
    cur = 0
    with open("FullmatrixList.txt", 'w') as f:
        #Don't uncomment this line, I'm using RTX 3090 on SLI to process
        #cp.cuda.Device(0,1).use()
        for row,col in cpSortedArr:
            if(cur != row):
                np.savetxt("FullmatrixList.txt", cp.asnumpy(arr),header="[", footer="]", newline=" ", fmt="%s")
                cur = row
                arr = cp.zeros(size, dtype="int32")
            arr[col.get()] = 1
        else:
            np.savetxt("FullmatrixList.txt", cp.asnumpy(arr), newline=" ", fmt="%s")

def CompressedAdjMatrix(arr1):
    size = cp.unique(arr1).size
    cpSortedArr = arr1[arr1[:,0].argsort()]

    arr = cp.zeros(size, dtype="int32")
    cur = 0
    with open("matrixList.txt", 'w') as f:
        #Don't uncomment this line, I'm using RTX 3090 on SLI to process
        #cp.cuda.Device(0,1).use()
        for row,col in cpSortedArr:
            if(cur != row):
                f.write(cp.array_str(arr) + "\n")
                cur = row
                arr = cp.zeros(size, dtype="int32")
            arr[col.get()] = 1
        else:
            f.write(cp.array_str(arr) + "\n")
            f.close() 

def ConvertToAdjList(arr1):
    cpSortedArr = arr1[arr1[:,0].argsort()]
    start,end = cp.hsplit(cpSortedArr, 2)
    node = cp.unique(cpSortedArr).size
 
    #cp.cuda.Device(0).use()
    adjList = [[] for k in range(node)]
    
    for i in range(node):
        u = int(start[i].get())
        v = int(end[i].get())
        adjList[u].append(v)
    
    np.savetxt("adjList.txt", adjList, delimiter=" ", fmt="%s")

if __name__=="__main__":
    nparray = ReadFile()

    cparray = cp.array(nparray)

    #WARNING! DO NOT RUN THIS LINE UNLESS YOU WANT FULL MATRIX (1 MILLION X 1 MILLION)
    #matrixList = FullAdjMatrix(cparray)
    #matrixList = CompressedAdjMatrix(cparray)

    #THIS LINE SHOULD BE OK FOR
    #adjList = ConvertToAdjList(cparray)
