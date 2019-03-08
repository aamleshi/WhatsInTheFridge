import numpy as np 
from tqdm import tqdm
import os
import random
from PIL import Image
import pickle
from tempfile import TemporaryFile
import skimage
import skimage.transform

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
        fullpath = [folderPath+ '/'+path for path in imagePathList]
        allImagePaths = allImagePaths + fullpath
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
    validIdx = int(np.ceil(len(allImagePaths)*validfrac))
    valid_features = allImagePaths[:validIdx]
    valid_labels = allImageLabel[:validIdx]
    train_features = allImagePaths[validIdx:]
    train_labels = allImageLabel[validIdx:]
    return (valid_features, valid_labels, train_features, train_labels)

def one_hot_encode(x):
    classes = ["Can", "Cookies", "Eggs", "Empty", "Fruit"]
    classEncoder = {classID:i for (i, classID) in enumerate(classes)}
    encoded = np.zeros((len(x), 5))
    for idx, val in enumerate(x):
        encoded[idx][classEncoder[val]] = 1       
    return encoded

def _preprocess_and_save(features, labels, folderpath):
    labels = one_hot_encode(labels)
    try:
        os.mkdir(folderpath)
    except:
        pass
    with open(folderpath+"/labels", 'wb') as f:
        pickle.dump( labels, f, protocol=2)
    for i, feature in enumerate(features):
        with open(folderpath+"/"+str(i),'wb') as f:
            np.save(f, feature)

def preprocess_and_save_data(imagePaths, labels, batchSize = 16):
    valid_features, valid_labels, train_features, train_labels = train_validate_split(imagePaths, labels)
    assert(len(valid_features) == len(valid_labels))
    assert(len(train_features) == len(train_labels))
    print(len(valid_features))
    n_batches = len(train_features)//batchSize

    batchPath = "batchedData/"

    print("N_batches: ", n_batches)
    #for batch_i in tqdm(range(1, n_batches + 1)):
    for batch_i in tqdm(range(1, 12)):
        batchStart = (batch_i - 1) * batchSize
        batchEnd = batchStart + batchSize

        featurePaths = train_features[batchStart:batchEnd]
        
        features = []
        for path in tqdm(featurePaths):
            pic = Image.open(path)
            pix = np.array(pic.getdata()).reshape(pic.size[1], pic.size[0], 3)
            feature = np.copy(pix).astype('float')
            tmpFeature = skimage.transform.resize(feature, (224, 224))
            tmpFeature = np.copy(tmpFeature).astype('uint8')        
            features.append(tmpFeature)
        labels = train_labels[batchStart:batchEnd]
        _preprocess_and_save(features, labels, batchPath+'preprocess_batch_' + str(batch_i) + '.p')
    
    print("saving validation")

    features = []
    for path in tqdm(valid_features):
            pic = Image.open(path)
            pix = np.array(pic.getdata()).reshape(pic.size[1], pic.size[0], 3)
            feature = np.copy(pix).astype('float')
            tmpFeature = skimage.transform.resize(feature, (224, 224))
            tmpFeature = np.copy(tmpFeature).astype('uint8')        
            features.append(tmpFeature)

    _preprocess_and_save(np.array(valid_features), np.array(valid_labels), batchPath+'preprocess_validation.p')
    _preprocess_and_save(np.array(valid_features), np.array(valid_labels), batchPath+'preprocess_testing.p')
    return n_batches

def main():
    classList = ["Can", "Cookies", "Eggs", "Empty", "Fruit"]
    imgDir = "./Classes/"
    allImagePaths, allImageLabel = aggregateFiles(classList, imgDir)
    print("Images Found: ", len(allImageLabel))
    print(allImagePaths[1])
    preprocess_and_save_data(allImagePaths, allImageLabel)

if __name__ == "__main__":
    main()