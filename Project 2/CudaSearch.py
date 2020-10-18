import numpy as np
import cupy as cp
from timeit import default_timer as timer    

def ReadFile():
    edge = np.loadtxt("roadNet-PA.txt", dtype="int32", skiprows=4)
    array = np.array(edge)
    return array

def ConvertToAdjMatrix(arr1):
    size = cp.unique(arr1).size
    
    cpSortedArr = arr1[arr1[:,0].argsort()]

    arr = cp.zeros(size, dtype="int32")
    print(arr)
    cur = -1
    with open("matrixList.txt", 'ab') as f:
        for row,col in cpSortedArr:
            if(cur != row):
                NpSortedArr = np.array(arr.get())
                np.savetxt("matrixList.txt", NpSortedArr, delimiter=" ", fmt="%s")
                cur = row
                arr = cp.zeros(size, dtype="int32")
            arr[row][col] = 1
        else:
            NpSortedArr = np.array(arr.get())
            np.savetxt("matrixList.txt", NpSortedArr, delimiter=" ", fmt="%s")
            

def ConvertToAdjList(arr1):
    cpSortedArr = arr1[arr1[:,0].argsort()]
    start,end = cp.hsplit(cpSortedArr, 2)
    n = cp.unique(cpSortedArr).size
 
    # create empty adjacency lists - one for each node - 
    # with a Python list comprehension
    adjList = [[] for k in range(n)]
    
    # # scan the arrays edge_u and edge_v
    for i in range(n):
        u = int(start[i].get())
        v = int(end[i].get())
        adjList[u].append(v)
    
    np.savetxt("adjList.txt", adjList, delimiter=" ", fmt="%s")
    print("Done")

if __name__=="__main__":
    start = timer() 
    nparray = ReadFile()
    print("Read File Done", timer()-start) 

    start = timer() 
    cparray = cp.array(nparray)
    print("Cuda Array Done", timer()-start)

    adjList = ConvertToAdjMatrix(cparray)
