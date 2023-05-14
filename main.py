import numpy as np
from skimage import io#, data
#import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import filedialog
#from PIL import Image, ImageTk

# Image uploaded by user
chosenImg = None

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

# photo_image()
#  takes a numpy image and converts to a tkinter PhotoImage
#  img -> input image
#  scalar -> new size of image in tkinter (should be the minimum of the width and height of canvas)
def photo_image(img, scalar):
    height, width = img.shape[:2]
    # encode and create PhotoImage object
    data = f'P6 {width} {height} 255 '.encode() + img.astype(np.int8).tobytes()
    img = tk.PhotoImage(width=width, height=height, data=data, format='PPM')
    # get longest edge of image
    multi = max(height, width)
    # scale image (values//100 to stop memory errors)
    img = img.zoom(scalar//100)
    img = img.subsample(multi//100)
    return img

def upload_file(canvas):
    ftypes = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'), ('Png Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=ftypes)
    global chosenImg
    chosenImg = io.imread(filename)
    i = photo_image(chosenImg, canvas)
    c_width = canvas.winfo_width()
    canvas.create_image(c_width//2,c_width//2, anchor=tk.CENTER, image=i)   
    canvas.image = i
    return

def show_result(canvas):
    # default block size if input is empty
    res = 24 if i1.get() == "" else int(i1.get())
    if chosenImg is not None:
        min_d = min(canvas.winfo_width(), canvas.winfo_height())
        out = generate(chosenImg, res)
        i = photo_image(out, min_d)
        c_width = canvas.winfo_width()
        c_height = canvas.winfo_height()
        canvas.create_image(c_width//2,c_height//2, anchor=tk.CENTER, image=i)   
        canvas.image = i
    return 

if __name__ == "__main__":
    # read image from file
    img = io.imread("colour.jpg")
    empty = io.imread("blank.jpg")
    # create filtered image
    filtered = extract_drawing(img, determine_limit(empty, True))
    out = generate(filtered, 24)

    root = tk.Tk()  
    width= root.winfo_screenwidth()               
    height= root.winfo_screenheight()  
    root.state("zoomed")
    #root.geometry("%dx%d" % (width, height))
    c_width = 2*width//3
    c_height = c_width//2
    canvas = tk.Canvas(root, width=width//3, height=height, highlightthickness=0, bg="red")   
    canvas1 = tk.Canvas(root, width=2*width//3, height=height, highlightthickness=0, bg="blue")  
    canvas2 = tk.Canvas(root, width=width//3, height=width//3, highlightthickness=0, bg="black")   
    canvas2.pack()
    canvas3 = tk.Canvas(root, width=width//3, height=height-(width//3), highlightthickness=0, bg="yellow")   
    canvas3.pack()
    canvas.create_window(0,0, anchor=tk.NW, window=canvas2)   
    canvas.create_window(0,width//3, anchor=tk.NW, window=canvas3)  
     
    #img = _photo_image(out, canvas)
    b = tk.Button(root, text='Upload File', command = lambda:[upload_file(canvas2)])
    b.pack()
    b1 = tk.Button(root, text='Generate Image', command = lambda:show_result(canvas1))
    b1.pack()
    
    l1 = tk.Label(root, text="Block Size")
    l1.pack()
    i1 = tk.Entry(root)
    i1.pack()
    canvas3.create_window(0,0, width=width//6, anchor=tk.NW, window=b) 
    canvas3.create_window(width//6,0, width=width//6, anchor=tk.NW, window=b1) 
    canvas3.create_window(0,40, anchor=tk.NW, window=l1) 
    canvas3.create_window(l1.winfo_reqwidth(),40, width=30, anchor=tk.NW, window=i1) 
    canvas.pack(side='left')  
    canvas1.pack(side='right')  
    
    
    
    tk.mainloop()  