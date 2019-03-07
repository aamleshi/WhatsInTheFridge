#!/usr/bin/env python3

import os
import math
from PIL import Image

def give_abs_paths(directory):
    """
    returns list of absolute filepaths for all files in given directory
    """
    filepaths = []
    for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           filepaths.append(os.path.abspath(os.path.join(dirpath, f)))
    return filepaths

def give_img_name(image_path):
    """
    returns name of file for given file path
    """
    name = os.path.splitext(os.path.basename(image_path))[0]
    return name

def give_crop_areas(rows, cols, img):
    """
    returns a list of 4-tuple arguments (x, y, x, y) used to crop images
    """
    if rows == 0 and cols == 0:
        return None

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

def crop_into_tiles(rows, cols, img):
    """
    crops an image into rows X cols number of tiles
    returns list of image tiles
    """
    areas = give_crop_areas(rows, cols, img)
    img_list = []
    for area in areas:
        cropped_img = img.crop(area)
        img_list.append(cropped_img)
    return img_list

def split_image(rows, cols, orig_img, orig_img_name):
    """
    creates a folder of sub-images split into rows X cols number of tiles and
    returns a list of absolute file paths of the sub-images
    """
    imgs = crop_into_tiles(rows, cols, orig_img)

    if not os.path.exists(orig_img_name):
        os.makedirs(orig_img_name)

    label = 0
    files = []
    for img in imgs:
        filename = orig_img_name + "/" + orig_img_name + "_" + str(label) + ".jpg"
        img.save(filename)
        files.append(os.path.abspath(filename))
        label += 1

    return files

def initial_shelf_crop(orig_img):
    """
    returns Image object with image cropped to remove noise (based on hardcoded values)
    """
    new_img = orig_img.crop((339, 478, 3211, 3990))

    (total_w, total_h) = new_img.size
    top_shelf_img = new_img.crop((0, 0, total_w, 1415))
    bottom_shelf_img = new_img.crop((0, 2093, total_w, total_h))

    (top_w, top_h) = top_shelf_img.size
    (bottom_w, bottom_h) = bottom_shelf_img.size

    final_img = Image.new('RGB', (max(top_w, bottom_w), top_h + bottom_h))

    final_img.paste(im=top_shelf_img, box=(0, 0))
    final_img.paste(im=bottom_shelf_img, box=(0, top_h))
    return final_img

def shelf_crop_file(image_path):
    """
    crops a single .jpg shelf image
    """
    orig_img = Image.open(image_path)
    orig_img_name = give_img_name(image_path)
    items_img = initial_shelf_crop(orig_img)

    img_files = split_image(2, 2, items_img, orig_img_name)
    for fname in img_files:
        print("created : ", fname)
    return 0

def shelf_crop_directory(dir):
    """
    crops a directory of .jpg shelf images
    """
    filenames = give_abs_paths(dir)
    for image_path in filenames:
        shelf_crop_file(image_path)

def consolidate_images():
    try:
        os.mkdir('./consolidated_images')
    except OSError:
        print("consolidated_images directory already exists, skipping")
    dirlist = os.listdir('./')
    for item in dirlist:
        if item.startswith('IMG'):
            inner_dirlist = os.listdir('./'+item)
            for inneritem in inner_dirlist:
                os.rename('./'+item+'/'+inneritem, './consolidated_images/'+inneritem)
            os.rmdir('./'+item)

def main():
    print("hello, this is split_image.py")
    dir = '../TrainingImages3-5'
    shelf_crop_directory(dir)
    consolidate_images()

if __name__ == main():
    main()
