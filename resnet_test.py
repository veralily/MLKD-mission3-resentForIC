# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Evaluation for CIFAR-10.
Accuracy:
cifar10_train.py achieves 83.0% accuracy after 100K steps (256 epochs
of data) as judged by cifar10_eval.py.
Speed:
On a single Tesla K40, cifar10_train.py processes a single batch of 128 images
in 0.25-0.35 sec (i.e. 350 - 600 images /sec). The model reaches ~86%
accuracy after 100K steps in 8 hours of training time.
Usage:
Please see the tutorial and website for how to download the CIFAR-10
data set, compile the program and train the model.
http://tensorflow.org/tutorials/deep_cnn/
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import math
import time
import os

import numpy as np
import tensorflow as tf

import resnet
import train_imagenet
import read_testdata

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('test_dir', '/tmp/resnet_test',
                           """Directory where to write event logs.""")
tf.app.flags.DEFINE_string('test_data', 'check_ic//check',
                           """Either 'test' or 'train_eval'.""")
tf.app.flags.DEFINE_string('checkpoint_dir', '/tmp/resnet_train',
                           """Directory where to read model checkpoints.""")
tf.app.flags.DEFINE_integer('eval_interval_secs', 60 * 5,
                            """How often to run the eval.""")
tf.app.flags.DEFINE_integer('num_examples', 100,
                            """Number of examples to run.""")
tf.app.flags.DEFINE_boolean('run_once', True,
                            """Whether to run eval only once.""")

resultfile = 'result.list'
write_results = open(resultfile, 'w+')


def evaluate():
    with tf.Graph().as_default() as g:
        files, images = read_testdata.distorted_inputs(FLAGS.test_data)
        num_iter = FLAGS.num_examples
        step = 0
        # print(images_t)

        images_placeholder = tf.placeholder(tf.float32, shape=(
            20, FLAGS.input_size, FLAGS.input_size, 3))
        logits_ = resnet.inference(
            images_placeholder, num_classes=12, is_training=False, bottleneck=False, num_blocks=[1, 1, 1, 1])
        logits = tf.nn.softmax(logits_)
        predictions_ = tf.argmax(logits, 1)
        predictions = tf.cast(predictions_, tf.int32)

        saver = tf.train.Saver()

        sess = tf.Session()
        sess2 = tf.Session()
        ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)

        if ckpt and ckpt.model_checkpoint_path:
            # Restores from checkpoint
            saver.restore(sess, ckpt.model_checkpoint_path)
            # Assuming model_checkpoint_path looks something like:
            #   /my-favorite-path/cifar10_train/model.ckpt-0,
            # extract global_step from it.
            global_step = ckpt.model_checkpoint_path.split(
                '/')[-1].split('-')[-1]
        else:
            print('No checkpoint file found')
            return
            # Calculate predictions.

        while step < num_iter:
            print("step")
            print(step)
            files_t = files[step]
            images_t = images[step]
            print("images_t")
            print(images_t)
            feed_dict = {images_placeholder: sess2.run(images_t)}
            print("feed_dict")
            #logits = sess.run(logits, feed_dict=feed_dict)
            #print("run logits")
            #print(logits)
            #print(files_t)
            results = sess.run(predictions, feed_dict=feed_dict)
            for (filename, result) in zip(files_t, results):
                filename = filename.split('/')[-1]
                filename = os.path.splitext(filename)[0]
                content = filename + '\t' + str(result + 1) + '\n'
                write_results.writelines(content)
            step += 1

        write_results.close()


def main(argv=None):  # pylint: disable=unused-argument
    if tf.gfile.Exists(FLAGS.test_dir):
        tf.gfile.DeleteRecursively(FLAGS.test_dir)
    tf.gfile.MakeDirs(FLAGS.test_dir)
    evaluate()


if __name__ == '__main__':
    tf.app.run()
