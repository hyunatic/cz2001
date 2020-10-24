import numpy as np
import cupy as cp
from timeit import default_timer as timer    

#I'm running on cupy-cuda11.0 
#Please also install CUDA toolkit, in order to execute cupy python library

def ReadFile():
    #Read VIA CPU and store into RAM
    edge = np.loadtxt("roadNet-PA.txt", dtype="int32", skiprows=4)
    array = np.array(edge)
    return array

def FullAdjMatrix(arr1):
    #Device 1 is Asus Strix RTX 3090
    #cp.cuda.Device(1).use()
    #Count number of nodes
    size = cp.unique(arr1).size
    #Sort in ascending [[0,1], [1,2], [0,2]] >> [[0,1], [0,2], [1,2]]
    cpSortedArr = arr1[arr1[:,0].argsort()]

    #Device 0 is MSI Gaming X Trio RTX 3090
    #cp.cuda.Device(0).use()
    #Initialize a [0,0,0,...,0] with a size of n in parallel
    arr = cp.zeros(size, dtype="int32")
    cur = 0
    #Don't uncomment this line, I'm using 2 GPU(s) on SLI to process
    #cp.cuda.Device({0,1}).use()
    with open("FullmatrixList.txt", 'w') as f:
        for row,col in cpSortedArr:
            if(cur != row):
                np.savetxt("FullmatrixList.txt", cp.asnumpy(arr),header="[", footer="]", newline=" ", fmt="%s")
                cur = row
                arr = cp.zeros(size, dtype="int32")
            arr[col.get()] = 1
        else:
            np.savetxt("FullmatrixList.txt", cp.asnumpy(arr),header="[", footer="]", newline=" ", fmt="%s")

def CompressedAdjMatrix(arr1):
    #Device 1 is Asus Strix RTX 3090
    #cp.cuda.Device(1).use()
    size = cp.unique(arr1).size
    cpSortedArr = arr1[arr1[:,0].argsort()]

    #Device 0 is MSI Gaming X Trio RTX 3090
    #cp.cuda.Device(0).use()
    #Initialize a [0,0,0,...,0] with a size of n in parallel
    arr = cp.zeros(size, dtype="int32")
    cur = 0

    #Don't uncomment this line, I'm using 2 GPU(s) on SLI to process
    #cp.cuda.Device({0,1}).use()
    with open("matrixList.txt", 'w') as f:
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
    #Device 1 is Asus Strix RTX 3090
    #cp.cuda.Device(1).use()
    cpSortedArr = arr1[arr1[:,0].argsort()]
    #Split [[1,2],[1,3],[1,4]] > start [1,1,1] end [2,3,4]
    start,end = cp.hsplit(cpSortedArr, 2)
    node = cp.unique(cpSortedArr).size
    
    #Device 0 is MSI Gaming X Trio RTX 3090
    #cp.cuda.Device(0).use()
    adjList = [[] for k in range(node)]

    #Line 52 ~ 58 are executed in parallel
    #Line 78 wait for both of my GPU to finish calculating for continuing to the next line
    #cp.cuda.Device({0,1}).synchronize()
    
    #Using both GPU to process at the same time
    #cp.cuda.Device({0,1}).use()
   
    for i in range(node):
        u = int(start[i].get())
        v = int(end[i].get())
        adjList[u].append(v)

    
    #np.savetxt("adjList.txt", adjList, delimiter=" ", fmt="%s")
    return adjList
    

def TransferToGpu(nparray):
    return cp.array(nparray)

if __name__=="__main__":
    #Read file data into RAM
    nparray = ReadFile()

    #Transfer data into the GPU
    cparray = TransferToGpu(nparray)

    #WARNING! DO NOT RUN THIS LINE UNLESS YOU WANT FULL MATRIX (1 MILLION X 1 MILLION)
    #matrixList = FullAdjMatrix(cparray)
    #matrixList = CompressedAdjMatrix(cparray)

    #THIS LINE SHOULD BE OK FOR
    #adjList = ConvertToAdjList(cparray)
