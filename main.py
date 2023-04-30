import numpy as np
from skimage import io, data
import matplotlib.pyplot as plt 

if __name__ == "__main__":
    img = io.imread("test.jpg")
    maskStrict = (img > 55).any(-1)
    maskForgiving = (img > 55).all(-1)
    height, width, d = img.shape
    out = np.empty(shape=(height, width, 3), dtype="int")
    
    out = img.copy()

    out[(maskStrict == True)] = 255
    
           
    io.imshow(out)
    plt.show()