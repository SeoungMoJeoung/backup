import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import models, layers, utils

def main():
	data = pd.read_csv("/home/mo/Project/BIO/raw_cassandra/raw193.csv")
	data = np.array(data)
	data = data[data[:,-1]!=0] # y = 0, raw remove
	data = data[data[:,-3]!=0]

	y_testReal = data[2700000:-1, -1]

	data_min = np.min(data, axis=0)
#	print(data_min[-4:-1])
	data_min[0] = 0
	data_min[1] = 0
	data_min = data_min
	print(data_min)
	data = data - data_min
	print(data)
#	x_train = data[:2281675, 1:-1]
#	y_train = data[:2281675, -1]

#	x_test = data[2281675:, 1:-1]
#	y_test = data[2281675:, -1]

	x_train = data[:2700000, 1:-1]
	y_train = data[:2700000, -1]

	x_test = data[2700000:-1, 1:-1]
	y_test = data[2700000:-1, -1]
	y_testReal = y_testReal.reshape(-1, 1)

#	x_train = x_train.astype(np.float64)
	y_train = y_train.reshape(-1, 1)
#	x_test = x_test.astype(np.float32)
	y_test = y_test.reshape(-1, 1)
#	print(x_train.shape)
#	print("x_train\n",x_train)
#	print("Y_train\n",y_train)
#	print("x_test\n",x_test)
#	print("y_test\n",y_test)

	model = linear_model(x_train, y_train)
	
	y_pred = model.predict(x_test).astype(np.float64)
	y_pred = y_pred + data_min[-1]
	print("Y_pred\n",y_pred)
	print("Y_test\n",y_testReal)
	
	error_mean = np.mean(np.abs(y_testReal - y_pred), axis=0)
	print('Error_mean:', error_mean)

def linear_model(X, Y):
	model = models.Sequential()
	model.add(layers.Dense(16, input_shape=(5,)))
	model.add(layers.Dense(32))
	model.add(layers.Dense(64))
	model.add(layers.Dense(128))
#	model.add(layers.Dense(256))
#	model.add(layers.Dense(512))
	model.add(layers.Dense(1,))

	model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
	model.fit(X, Y, epochs = 10, batch_size = 32)
	
#	Y_pred = model.predict(X_test)
#	print("Y_pred\n",Y_pred)
#	print("Y_test\n",Y_test)

#	error_mean = np.mean(np.abs(Y_test - Y_pred), axis=0)
#	print('Error_mean:', error_mean)

	return model

main()
