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
tf.app.flags.DEFINE_string('data_dir', 'ic-data//train',
                           'data dir')
tf.app.flags.DEFINE_string('extra_dir', 'ic-data//extra', 'extra dir')
tf.app.flags.DEFINE_string('train_label', 'train.label', 'train label')
tf.app.flags.DEFINE_string('extra_label', 'extra.label', 'extra label')
tf.app.flags.DEFINE_string('extra1_label', 'extra1.label', 'extra1 label')
tf.app.flags.DEFINE_string('extra2_label', 'extra2.label', 'extra2 label')


def file_list(data_dir):
    filenames = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                filenames.append(file)
    return filenames


def load_data(data_dir, label_file):
    data = []
    i = 0

    print "listing files in", data_dir
    start_time = time.time()
    files = file_list(data_dir)
    labelname = os.path.join(data_dir, label_file)
    labels_map = {}
    label_reader = open(labelname)
    labels_content = label_reader.readlines()
    for i, label_content in enumerate(labels_content):
        label_index = label_content.split(' ')[0]
        label = label_content.split(' ')[1]
        img_fn = os.path.join(data_dir, label_index + '.jpg')
        data.append({
            "filename": img_fn,
            "label_name": label,
            "label_num": int(label) - 1})
        labels_map[label_index] = {"order": i + 1, "label": label}

    duration = time.time() - start_time
    label_reader.close()
    print "took %f sec" % duration
    return data


def distorted_inputs(train):
    train_data = load_data(FLAGS.data_dir, FLAGS.train_label)
    '''extra1_data = load_data(FLAGS.extra_dir, FLAGS.extra1_label)
    print(len(extra1_data))
    extra2_data = load_data(FLAGS.extra_dir, FLAGS.extra2_label)
    print(len(extra2_data))'''
    extra_data = load_data(FLAGS.extra_dir, FLAGS.extra_label)

    if train:
        train_data[len(train_data): len(train_data)] = extra_data
        data = train_data
    else:
        data = extra_data

    filenames = [d['filename'] for d in data]
    label_nums = [d['label_num'] for d in data]

    filename, label_num = tf.train.slice_input_producer(
        [filenames, label_nums], shuffle=True)

    num_preprocess_threads = 4
    images_and_labels = []
    for thread_id in range(num_preprocess_threads):
        image_buffer = tf.read_file(filename)

        bbox = []
        train = True
        image = image_preprocessing(image_buffer, bbox, train, thread_id)
        images_and_labels.append([filename, image, label_num])

    files, images, label_index_batch = tf.train.batch_join(
        images_and_labels,
        batch_size=FLAGS.batch_size,
        capacity=2 * num_preprocess_threads * FLAGS.batch_size)

    height = FLAGS.input_size
    width = FLAGS.input_size
    depth = 3

    images = tf.cast(images, tf.float32)
    images = tf.reshape(images, shape=[FLAGS.batch_size, height, width, depth])

    files = tf.reshape(files, [FLAGS.batch_size])

    return files, images, tf.reshape(label_index_batch, [FLAGS.batch_size])


def main(_):
    _, images, labels = distorted_inputs(train=True)
    print(labels)

    train(is_training=True, images=images, labels=labels)

if __name__ == '__main__':
    tf.app.run()
