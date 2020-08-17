import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import models, layers, utils

def main():
	data = pd.read_csv("/home/mo/Project/BIO/flow.csv")
	data = np.array(data)
	print(data.shape)
	print(data)
	x_train = data[:25000, 3:]
	y_train = data[:25000, 0]
	#8127
	x_test = data[25000:, 3:]
	y_test = data[25000:, 0]

	x_train = x_train.astype(np.float32)
	y_train = y_train.reshape(-1, 1).astype(np.float32)
	x_test = x_test.astype(np.float32)
	y_test = y_test.reshape(-1, 1).astype(np.float32)
	print(x_train)
	print(y_train)

	linear_model(x_train, y_train, x_test, y_test)

def linear_model(X, Y, X_test, Y_test):
	model = models.Sequential()
	model.add(layers.Dense(16, input_shape=(5,)))
	model.add(layers.Dense(32))
	model.add(layers.Dense(64))
	model.add(layers.Dense(128))
#	model.add(layers.Dense(256))
#	model.add(layers.Dense(512, activation = 'relu'))
	model.add(layers.Dense(1,))

	model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
	model.fit(X, Y, epochs = 100, batch_size = 32)
	
	Y_pred = model.predict(X_test)
	print(Y_pred)
	print(Y_test)

	error_mean = np.mean(np.abs(Y_test - Y_pred), axis=0)
	print('Error_mean:', error_mean)

main()
