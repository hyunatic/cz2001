import cupy as cp
import time

iterations = 1000000
loops = 10;
stack = iterations // loops

a = cp.random.rand(stack,44,20)
b = cp.random.rand(stack,20,1)

def ab(a,b,iterations):
    for i in range(iterations):
        cp.matmul(a,b,out=None)

t1 = time.time()
ab(a,b,loops)
t2 = time.time()
total = t2-t1
print(total)
