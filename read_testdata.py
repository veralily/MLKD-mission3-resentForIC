import skimage.io  # bug. need to import this before tensorflow
import skimage.transform  # bug. need to import this before tensorflow
from resnet_train import train
from resnet import inference
import tensorflow as tf
import time
import os
import sys
import re
import numpy as np

from image_processing import image_preprocessing

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('filename_list', 'check.doc.list', 'file list')


'''def file_list(filename_list):
    reader = open(filename_list, 'r')
    filenames = reader.readlines()
    filenames = [int(f) for f in filenames]
    return filenames'''


def file_list(data_dir):
    i = 0
    filenames = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                filename = os.path.splitext(file)[0]
                i = i + 1
                filenames.append(int(filename))
    print("number of files")
    print(i)
    return filenames


def load_data(data_dir):
    data = []

    start_time = time.time()
    files = file_list(data_dir)

    duration = time.time() - start_time
    print "took %f sec" % duration

    for img_fn in files:
        img_fn = str(img_fn) + '.jpg'
        fn = os.path.join(data_dir, img_fn)

        data.append(fn)

    return data


def distorted_inputs(data_dir):
    filenames = load_data(data_dir)
    files = []
    images = []
    i = 0
    files_b = []
    images_b = []


    height = FLAGS.input_size
    width = FLAGS.input_size
    depth = 3
    step = 0

    for filename in filenames:       
        image_buffer = tf.read_file(filename)
        bbox = []
        train = False
        image = image_preprocessing(image_buffer, bbox, train, 0)
        files_b.append(filename)
        images_b.append(image) 
        i = i + 1      
        #print(image)
        if i == 20:
            print(i)
            files.append(files_b)
            images_b = tf.reshape(images_b, [20, height, width, depth])
            images.append(images_b)
            files_b = []
            images_b = []
            i = 0

    #files = files_b
    #images = tf.reshape(images_b, [13, height, width, depth])
        

        

    

    images = np.array(images, ndmin=1)

    #images = tf.cast(images, tf.float32)

    #images = tf.reshape(images, shape=[-1, height, width, depth])
    print(type(files))
    print(type(images))
    print(images.shape)
    #files = tf.reshape(files, [len(files)])

    # print(files)
    # print(images)

    return files, images

_, images = distorted_inputs("check_ic//check")
