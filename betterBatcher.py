import numpy as np 
from tqdm import tqdm
import os
import random


def aggregateFiles(classList, imgDir, shuffle= True):
    """
    Inputs: ClassList, ImagePath
    Outputs: List of all images, Corresponding list of labels
    """
    allImagePaths = []
    allImageLabel = []
    for classID in tqdm(classList):
        folderPath = imgDir + classID
        imagePathList = os.listdir(folderPath)
        allImagePaths = allImagePaths + imagePathList
        allImageLabel = allImageLabel + [classID]*len(imagePathList)
    if shuffle:
        c = list(zip(allImagePaths, allImageLabel))
        random.shuffle(c)
        allImagePaths, allImageLabel = zip(*c)
    return allImagePaths, allImageLabel

def train_validate_split(allImagePaths, allImageLabel, validfrac = .1):
    valid_features = []
    valid_labels = []
    train_features = []
    train_labels = []
    assert(len(allImageLabel) == len(allImagePaths))
    validIdx = np.ciel(len(allImagePaths)*validfrac)
    valid_features = allImagePaths[:validIdx]
    valid_labels = allImageLabel[:validIdx]
    valid_features = allImagePaths[validIdx:]
    valid_labels = allImageLabel[validIdx:]
    return (valid_features, valid_labels, train_features, train_labels)

def one_hot_encode(x):
    classEncoder = {classID:i for (i, classID) in enumerate(classes)}
    encoded = np.zeros((len(x), 5))
    for idx, val in enumerate(x):
        encoded[idx][classEncoder[val]] = 1       
    return encoded

def _preprocess_and_save(features, labels, filename):
    labels = one_hot_encode(labels)
    pickle.dump((features, labels), open(filename, 'wb'))

def preprocess_and_save_data(imagePaths, labels, batchSize = 16):
    valid_features, valid_labels, train_features, train_labels = train_validate_split(imagePaths, labels)
    assert(len(valid_features) == len(valid_labels))
    assert(len(train_features) == len(train_labels))
    n_batches = len(train_features)//batchSize

    batchPath = "batchedImages/"

    for batch_i in tqdm(range(1, n_batches + 1)):
        batchStart = (batch_i - 1) * batchSize
        batchEnd = batchStart + batchSize
        features = train_features[batchStart:batchEnd]
        labels = train_labels[batchStart:batchEnd]
        
        # find index to be the point as validation data in the whole dataset of the batch (10%)

        # preprocess the 90% of the whole dataset of the batch
        # - normalize the features
        # - one_hot_encode the lables
        # - save in a new file named, "preprocess_batch_" + batch_number
        # - each file for each batch
        _preprocess_and_save(features, labels, 
                             batchPath+'preprocess_batch_' + str(batch_i) + '.p')
    _preprocess_and_save(np.array(valid_features), np.array(valid_labels),
                         batchPath+'preprocess_validation.p')
    _preprocess_and_save(np.array(valid_features), np.array(valid_labels),
                         batchPath+'preprocess_testing.p')


def main():
    classList = ["Can", "Cookies", "Eggs", "Empty", "Fruit"]
    imgDir = "./Classes/"
    allImagePaths, allImageLabel = aggregateFiles(classList, imgDir)
    print("Images Found: ", len(allImageLabel))
    print("TODO")

if __name__ == "__main__":
    main()