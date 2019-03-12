#!/usr/bin/env python3

import sys
from PIL import Image
from split_image import *
import pyfiglet
import tqdm
import numpy as np 
import os
from tqdm import tqdm
import skimage.io
import skimage.transform
import tensorflow as tf


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
    predictions = run_ml(img_files)


    #testing arbitrary class strings, delete when done
    sub_img_A = "Cookies"
    sub_img_B = "Can"
    sub_img_C = "Fruit"
    sub_img_D = "Can"
    sub_imgs = [sub_img_A, sub_img_B, sub_img_C, sub_img_D]

    classes = count_items(predictions)
    print_fridge_contents(classes)

def load_label_names():
    return ["Can", "Cookies", "Eggs", "Empty", "Fruit"]

def run_ml(imageFiles):

    #format the images

    features = []
    for path in tqdm(imageFiles):
        pic = Image.open(path)
        pix = np.array(pic.getdata()).reshape(pic.size[1], pic.size[0], 3)
        feature = np.copy(pix).astype('float')
        tmpFeature = skimage.transform.resize(feature, (224, 224))
        tmpFeature = np.copy(tmpFeature).astype('uint8')        
        features.append(tmpFeature)
    labels = ['1']*len(features)


    #load the model
    config = tf.ConfigProto(
        device_count = {'GPU': 0}
    )
    loaded_graph = tf.Graph()
    save_model_path = './image_classification'
    label_names = load_label_names()
    with tf.Session(config=config, graph=loaded_graph) as sess:
        loader = tf.train.import_meta_graph(save_model_path + '.meta', clear_devices=True)
        loader.restore(sess, save_model_path)

        loaded_x = loaded_graph.get_tensor_by_name('input_x:0')
        loaded_y = loaded_graph.get_tensor_by_name('output_y:0')
        loaded_logits = loaded_graph.get_tensor_by_name('logits:0')
        loaded_acc = loaded_graph.get_tensor_by_name('accuracy:0')

        test_predictions = sess.run(
            tf.nn.softmax(loaded_logits),
            feed_dict={loaded_x: features})
            #feed_dict={loaded_x: features, loaded_y: labels})
        predNames = []
        for pred in test_predictions:
            predNames.append(label_names[np.argmax(pred)])
        return(predNames)
    #return the class label


def main():
    demo("./TrainingImages3-5/IMG_20190306_000226.jpg")

if __name__ == main():
    main()
