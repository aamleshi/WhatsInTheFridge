#!/usr/bin/env python3

import sys
from PIL import Image
from split_image import *
import pyfiglet

def count_items(class_list):
    """
    class_list - a list of strings representing classes identified
    Returns dictionary with item count
    """
    classes = {"Cookies": 0, "Can": 0, "Fruit": 0, "Eggs": 0, "Empty": 0}
    for class_str in class_list:
        if class_str == "Cookies":
            classes["Cookies"] += 1
        elif class_str == "Can":
            classes["Can"] += 1
        elif class_str == "Fruit":
            classes["Fruit"] += 1
        elif class_str == "Eggs":
            classes["Eggs"] += 1
        elif class_str == "Empty":
            classes["Empty"] += 1

    return classes

def print_fridge_contents(classes):
    print("Your fridge contains:")
    for key, val in classes.items():
        if key == "Empty" and val == 4:
            print(pyfiglet.figlet_format("Nothing"))
        elif key != "Empty" and val > 0:
            print(pyfiglet.figlet_format(key + "  :  " + str(val)))

    print(pyfiglet.figlet_format("Enjoy!", font="utopia"))

def demo(image_path):
    """
    takes in single image
    """
    orig_img = Image.open(image_path)
    orig_img_name = give_img_name(image_path)
    items_img = initial_shelf_crop(orig_img)

    # list of absolute filepaths to each sub image
    img_files = split_image(2, 2, items_img, orig_img_name)

    #insert ML

    #testing arbitrary class strings, delete when done
    sub_img_A = "Cookies"
    sub_img_B = "Can"
    sub_img_C = "Fruit"
    sub_img_D = "Can"
    sub_imgs = [sub_img_A, sub_img_B, sub_img_C, sub_img_D]

    classes = count_items(sub_imgs)
    print_fridge_contents(classes)

def main():
    demo("./TrainingImages3-5/IMG_20190305_235230.jpg")

if __name__ == main():
    main()
