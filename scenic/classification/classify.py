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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import sys

import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

INPUT_DIR = './scenic/classification/models/'

flags = tf.app.flags

flags.DEFINE_string('model_dir', INPUT_DIR, 'Path to the model')
flags.DEFINE_string('output_labels', INPUT_DIR + 'output_labels.txt', 'Where to save the trained graph\'s labels')
flags.DEFINE_string('final_tensor_name', 'final_result',
                    'The name of the output classification layer in the retrained graph')
flags.DEFINE_string('output_graph', INPUT_DIR + 'output_graph.pb', 'Where to save the trained graph')
flags.DEFINE_integer('image_size', 224, 'The width and height of the input images')

FLAGS = flags.FLAGS

INITIAL_FLAG = False

GRAPH = None
LABELS = None

OUTPUT_TENSOR = None
RESIZED_IMAGE_TENSOR = None

# Infomations about the model to be used
MODEL_INFO = {
    'input_width': FLAGS.image_size,
    'input_height': FLAGS.image_size,
    'input_depth': 3,
    'resized_input_tensor_name': 'input:0',
    'output_tensor_name': FLAGS.final_tensor_name + ':0',
    'model_file_name': 'output_graph.pb',
    'input_mean': 127.5,
    'input_std': 127.5,
}


def create_model_graph(model_dir):
    """"Creates a graph from saved GraphDef file and returns a Graph object.

    Returns:
      Graph holding the trained Inception network, and various tensors we'll be
      manipulating.
    """
    with tf.Graph().as_default() as graph:
        global OUTPUT_TENSOR
        global RESIZED_IMAGE_TENSOR

        model_path = os.path.join(model_dir, MODEL_INFO['model_file_name'])
        with gfile.FastGFile(model_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            OUTPUT_TENSOR, RESIZED_IMAGE_TENSOR = (
                tf.import_graph_def(
                    graph_def,
                    name='',
                    return_elements=[
                        MODEL_INFO['output_tensor_name'],
                        MODEL_INFO['resized_input_tensor_name'],
                    ]))
    return graph


def get_final_result(sess, image_data, image_data_tensor,
                     decoded_image_tensor):
    global OUTPUT_TENSOR
    global RESIZED_IMAGE_TENSOR

    resized_input_values = sess.run(decoded_image_tensor,
                                    {image_data_tensor: image_data})
    final_result = sess.run(OUTPUT_TENSOR,
                            {RESIZED_IMAGE_TENSOR: resized_input_values})
    final_result = np.squeeze(final_result)

    return final_result


def add_jpeg_decoding(input_width, input_height, input_depth, input_mean,
                      input_std):
    """Adds operations that perform JPEG decoding and resizing to the graph..

    Args:
      input_width: Desired width of the image fed into the recognizer graph.
      input_height: Desired width of the image fed into the recognizer graph.
      input_depth: Desired channels of the image fed into the recognizer graph.
      input_mean: Pixel value that should be zero in the image for the graph.
      input_std: How much to divide the pixel values by before recognition.

    Returns:
      Tensors for the node to feed JPEG data into, and the output of the
        preprocessing steps.
    """
    jpeg_data = tf.placeholder(tf.string, name='DecodeJPGInput')
    decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
    decoded_image_as_float = tf.cast(decoded_image, dtype=tf.float32)
    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
    resize_shape = tf.stack([input_height, input_width])
    resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
    resized_image = tf.image.resize_bilinear(decoded_image_4d,
                                             resize_shape_as_int)
    offset_image = tf.subtract(resized_image, input_mean)
    mul_image = tf.multiply(offset_image, 1.0 / input_std)
    return jpeg_data, mul_image


def read_labels(label_path):
    label_file = open(label_path, 'r', encoding='utf-8')
    labels = [line[:-1] for line in label_file.readlines()]
    return labels


def initial():
    global GRAPH, LABELS, INITIAL_FLAG
    GRAPH = create_model_graph(FLAGS.model_dir)
    LABELS = read_labels(FLAGS.output_labels)
    INITIAL_FLAG = True


def classify(image):
    global INITIAL_FLAG
    if not INITIAL_FLAG:
        initial()

    global GRAPH, LABELS
    image_data = image
    class_count = len(LABELS)

    if class_count == 0:
        tf.logging.error('No valid classes of images')
        return -1

    with tf.Session(graph=GRAPH) as sess:
        # Set up the image decoding sub-graph.
        jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(
            MODEL_INFO['input_width'], MODEL_INFO['input_height'],
            MODEL_INFO['input_depth'], MODEL_INFO['input_mean'],
            MODEL_INFO['input_std'])

        final_result = get_final_result(sess, image_data, jpeg_data_tensor,
                                        decoded_image_tensor)
        return final_result
        # classification_result = LABELS[np.argmax(final_result)]
        # return classification_result


def classify_top1(image):
    final_result = classify(image)
    argmax = np.argmax(final_result)
    return LABELS[argmax], final_result[argmax]


def classify_top_n(image, n):
    final_result = classify(image)
    n_argmax = np.array(final_result).argsort()[-n:][::-1]
    result_list = []
    result_probability = []
    for arg in n_argmax:
        result_list.append(LABELS[arg])
        result_probability.append(final_result[arg])

    return result_list, result_probability


def main(argv):
    # Needed to make sure the logging output is visible.
    # See https://github.com/tensorflow/tensorflow/issues/3047
    tf.logging.set_verbosity(tf.logging.INFO)

    if len(argv) < 2:
        tf.logging.error('no images specified')
        return 1

    for image in argv[1:]:
        image_data = gfile.FastGFile(image, 'rb').read()
        classification_result, _ = classify_top1(image_data)
        print(image, ' is ', classification_result)

    '''
    class_count = len(labels)
    if class_count == 0:
      tf.logging.error('No valid classes of images')
      return -1
  
    with tf.Session(graph=graph) as sess:
      # Set up the image decoding sub-graph.
      jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(
          MODEL_INFO['input_width'], MODEL_INFO['input_height'],
          MODEL_INFO['input_depth'], MODEL_INFO['input_mean'],
          MODEL_INFO['input_std'])
  
  
      final_result = get_final_result(sess, labels, image_data, 
                                      jpeg_data_tensor, decoded_image_tensor)
      classfication_result = labels[np.argmax(final_result)]
      print(classfication_result)
      '''


if __name__ == '__main__':
    tf.app.run(main=main, argv=sys.argv)
