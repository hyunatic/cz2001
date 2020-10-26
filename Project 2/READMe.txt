Please install the NVIDIA toolkit in order for the CuPY library to run properly
Worst case scenario, If you don't want to install CuPy, use the numpy library instead of the cupy. 
After changing the library, the time complexity will increase drastically

Note: Time complexity heavily depends on the hardware and number of CUDA cores in the GPU. I'm running on 2x RTX 3090
with 10496 * 2 CUDA Cores