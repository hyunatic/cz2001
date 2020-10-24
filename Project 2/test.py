def FullAdjMatrix(arr1):
    #This is Out of Memory execption on with 3 million points
    size = max(max(arr1))+1
    r = [[0 for i in range(size)] for j in range(size)] # n^2
    
    for row,col in arr1: #n
        r[row][col] = 1
    print(r)