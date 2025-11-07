import numpy as np

a = [0.125,0.25,0.375,0.5,0.625,0.75,0.875,1]

fft_a = np.fft.fft(a)
print(fft_a)