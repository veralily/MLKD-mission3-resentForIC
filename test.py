import tensorflow as tf
a = [7,1,10,2,6]
b = [4,2,5,9,9]
val = tf.equal(a,b)
with tf.Session() as sess:
	print(val.eval())