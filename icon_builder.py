from time import sleep
from PIL import Image
from PIL import ImageOps
from pathlib import Path
import sys
import os
from common import *

GREEN_RANGE_MIN_HSV = (90, 80, 70)
GREEN_RANGE_MAX_HSV = (180, 255, 255)
ALPHA = (0,0,0,0)
VERSION = "0.13-path-1"
TITLE = f'Relicta Icon Builder v{VERSION}\nCreated by Astra (path by Yodes)'
LOGGER_FILE = "log.txt"
OUTPUT_FOLDER = "icon_output"
FILE_REG = ["*.png"]

def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v

def ProcessImage(image):
    pix = image.load()
    width, height = image.size
    left = width
    top = height
    right = 0
    bottom = 0
    for x in range(width):
        for y in range(height):
            r, g, b, a = pix[x, y]
            h_ratio, s_ratio, v_ratio = rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            h, s, v = (h_ratio * 360, s_ratio * 255, v_ratio * 255)

            min_h, min_s, min_v = GREEN_RANGE_MIN_HSV
            max_h, max_s, max_v = GREEN_RANGE_MAX_HSV
            if min_h <= h <= max_h and min_s <= s <= max_s and min_v <= v <= max_v:
                pix[x, y] = ALPHA
            else:
                if(x < left):
                    left = x
                if(x > right):
                    right = x
                if(y < top):
                    top = y
                if(y > bottom):
                    bottom = y           
    h = bottom - top
    w = right - left
    return image.crop((left,top,right,bottom))   
    
def main():
    if len(sys.argv) == 1:
        return -999

    to_convert = sys.argv[1]
    autosize = False
    paramsize = 0
    if len(sys.argv) == 3:
        autosize = True
        paramsize = int(sys.argv[2])
        print(f"Autosize enabled; size set to {paramsize}")
    # check for path
    if not IsPathExists(to_convert):
        print("Error. This path doesn't exist.")
        return -5

    # path collection
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    root = os.path.dirname(to_convert)
    logger = os.path.join(root,LOGGER_FILE)
    to_output = os.path.join(application_path,OUTPUT_FOLDER)
    paths = CollectFilePaths(to_convert,FILE_REG)

    # delete logger if exists
    DeleteFileIfExists(logger)

    # check if folder contains images
    if(len(paths) == 0):
        print(f'Error. This folder doesn\'t contain {FILE_REG} files.')
        return -1

    # resizing options
    to_size = 600
    if autosize:
        to_size = paramsize
    else:
        to_size = input("Enter size to which to resize images inbetween steps. Improves accuracy (default=600)\n")
        if not to_size.isnumeric():
            to_size = 600
        else:
            to_size = int(to_size)

    # process images
    i = 0
    errors = 0
    print("Start processing images...")
    sleep(3)
    DrawProgress(TITLE, i, len(paths), 40, errors)
    for path in paths:
        p = Path(path)
        rel = p.relative_to(to_convert)
        save_path = os.path.join(to_output,rel)    
        MakeDirsIfNotExist(save_path)

        im = Image.open(path)
        im = im.convert('RGBA')
        im = ImageOps.scale(im,to_size/im.width,Image.BICUBIC)
        try:
            im = ProcessImage(im)
        except ValueError:
            WriteToLog(logger,f'Picture {i+1} ({rel}): ValueError in crop(). Picture must be empty or object color got it erased.\n')
            errors += 1
            i += 1
            DrawProgress(TITLE, i, len(paths), 40, errors)
            continue
        else:
            if im.width < im.height:
                im = ImageOps.scale(im,128/im.height,Image.BICUBIC)
            else:
                im = ImageOps.scale(im,128/im.width,Image.BICUBIC)  
            im = ImageOps.pad(im,(128,128),Image.BICUBIC)
            im.save(save_path)
            i += 1
            DrawProgress(TITLE, i, len(paths), 40, errors)    
    
    DrawComplete()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())