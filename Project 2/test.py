import cupy as cp

arr2D = cp.array([[21,7,23,14], [11,10,33,7] ,[11,12,13,22]])
sorting = arr2D[arr2D[:,0].argsort()]
print('2D Numpy Array')
print(sorting)
