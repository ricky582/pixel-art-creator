import numpy as np
from skimage import io, data
import matplotlib.pyplot as plt 
import tkinter as tk
from PIL import Image, ImageTk

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

# generate()
#  takes an image and attempts to reduce it to "pixels" of specified size
#  img -> input image
#  step -> width of "pixels"
#  cap -> if the average value of all the RBG channels is above cap, they will be made fully white to avoid noise
#  binary -> if true, all pixels will either be made black (0,0,0) or white (255,255,255) based on cap
def generate(img, step, cap=150, binary=False):
    # get width and height of image
    h, b, _ = img.shape
    # trim off excess pixels to get an empty image of (h/step) by (b/step)
    h -= h%step
    b -= b%step
    out = np.zeros((h,b,3), dtype=int)
    # reshape image to 4D array of "pixels"
    regions = img[:h, :b].reshape(h//step, step, b//step, step, 3)
    # calculate mean color of each "pixel"
    means = np.mean(regions, axis=(1,3))
    # reshape array back to out size
    means = means.repeat(step, axis=0).repeat(step, axis=1)
    # convert array to int
    out = means.astype(int)
    # trim off noise from image (faint "pixels")
    out[(out > cap).any(-1)] = 255
    # make all remaining pixels black (0,0,0) 
    out[binary and (out < 255).all(-1)] = 0
    return out

def _photo_image(image, canvas):
    height, width = image.shape[:2]
    data = f'P6 {width} {height} 255 '.encode() + image.astype(np.int8).tobytes()
    img = tk.PhotoImage(width=width, height=height, data=data, format='PPM')
    img = img.subsample(4)
    c_width = canvas.winfo_width()
    print(c_width)
    canvas.create_image(c_width//2,height//8, anchor=tk.CENTER, image=img)   
    return img

if __name__ == "__main__":
    # read image from file
    img = io.imread("colour.jpg")
    empty = io.imread("blank.jpg")
    # create filtered image
    filtered = extract_drawing(img, determine_limit(empty, True))
    out = generate(filtered, 24)
    # show new image
    #io.imshow(out)
    #plt.show()
    root = tk.Tk()      
    canvas = tk.Canvas(root, width=1000, height=1000)      
    canvas.pack()      
    canvas.update()
    img = _photo_image(out, canvas)
   
    tk.mainloop()  