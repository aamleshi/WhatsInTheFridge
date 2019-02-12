#!/usr/bin/env python3

import os
import math
from PIL import Image

def give_crop_areas(rows, cols, image_path):
    """
    returns a list of 4-tuple arguments describing an area of the image

    rows - number of rows to partition the image into
    cols - number of columns to partition the image into
    image_path - filepath of image
    """
    if rows == 0 and cols == 0:
        return None

    img = Image.open(image_path)
    areas = []
    width = img.size[0]
    length = img.size[1]
    pix_col = math.floor(width/cols)
    pix_row = math.floor(length/rows)

    for x in range(0, rows):
        for y in range(0, cols):
            area = (x*pix_col, y*pix_row, (x+1)*pix_col, (y+1)*pix_row)
            areas.append(area)

    return areas

def crop(areas, image_path):
    """
    returns a list of sub-images that add up to the original image

    areas - list of 4-tuple arguments describing areas to partition
    the image into
    image_path - filepath of image
    """
    img = Image.open(image_path)
    img_list = []
    for area in areas:
        cropped_img = img.crop(area)
        img_list.append(cropped_img)
    return img_list

def split_image(rows, cols, image_path):
    """
    creates a folder of sub-images split into rows X cols number of tiles and
    returns a list of absolute file paths of the sub-images
    """
    crop_areas = give_crop_areas(rows, cols, image_path)
    imgs = crop(crop_areas, image_path)

    name = os.path.splitext(os.path.basename(image_path))[0]
    if not os.path.exists(name):
        os.makedirs(name)
    directory = name
    label = 0
    files = []

    for img in imgs:
        filename = directory + "/" + name + "_" + str(label) + ".jpg"
        img.save(filename)
        files.append(os.path.abspath(filename))
        label += 1

    return files

def main():
    rows = 4
    cols = 4

    image_path = "testimages/tree.jpg"
    img_files = split_image(rows, cols, image_path)
    for f in img_files:
        print("created : " + f)

if __name__ == main():
    main()
