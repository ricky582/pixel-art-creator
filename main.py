import numpy as np
from skimage import io, data
import matplotlib.pyplot as plt 

# extract_drawing()
#  takes an image, and filters all pixels lighter than limit (i.e. RGB value > limit), changing them to be white
#  img -> input image
#  limit -> limit to brightness of pixel
#  strict -> if true pixel is filtered if any of the RBG channels > limit, if false all channels must be > limit
def extract_drawing(img, limit, strict=True):
    # create mask
    if strict:
        mask = (img > limit).any(-1)
    else: 
        mask = (img > limit).all(-1)
    # copy input image (read only otherwise)
    out = img.copy()
    # turn all pixels to white where mask == True
    out[mask] = 255
    return out

# determine_limit()
#  takes an image of an empty and attempts to determine a suitable limit for filtering
#  img -> input image
#  lined -> for lined paper, results may not be as good
def determine_limit(img, lined=False):
    # remove all pixels of a certain level of "whiteness"
    if lined:
        img = img[img<85]
    # return mean of pixels
    return np.mean(img)

def generate(img, step):
    h, b, d = img.shape
    h = h - h%step
    b = b - b%step
    out = np.zeros((h,b,3), dtype=int)
    for i in range(0, int(h/step)):
        for j in range(0, int(b/step)):
            total = np.array([0,0,0], dtype=int)
            count = 0
            whites = 0
            for i1 in range(0, step):
                for j1 in range(0,step):
                    p = img[i*step+i1][j*step+j1]
                    #if p != (255,255,255):
                    total += p
                    count += 1
            new_p = np.floor_divide(total, count)
            new_p = new_p.astype(int)
            for i1 in range(0, step):
                for j1 in range(0,step):
                    out[i*step+i1][j*step+j1] = new_p               
    return out

if __name__ == "__main__":
    # read image from file
    img = io.imread("test.jpg")
    empty = io.imread("blank.jpg")
    # create filtered image
    filtered = extract_drawing(img, determine_limit(empty, True))
    out = generate(filtered, 24)
    # show new image
    io.imshow(out)
    plt.show()