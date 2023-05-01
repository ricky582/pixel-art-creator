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
#  takes an image and attempts to determine a suitible limit for filtering
#  img -> input image
def determine_limit(img):
    img = img[img<85]
    print(np.mean(img))
    return np.mean(img)

if __name__ == "__main__":
    # read image from file
    img = io.imread("test.jpg")
    empty = io.imread("blank.jpg")
    # create filtered image
    filtered = extract_drawing(img, determine_limit(empty))
    # show new image
    io.imshow(filtered)
    plt.show()