import numpy as np
from skimage import io
import matplotlib.pyplot as plt 

if __name__ == "__main__":
    img = io.imread("test.jpg")
    io.imshow(img)
    plt.show()