import numpy as np

ints = [[9,9], [8,8], [10,10], [12,12], [20,20]]
arr = np.array(ints)
solution = np.argwhere(arr == 9)
print(solution)
for i,j in solution:
     print(i,j)