# 만든이 : 정성모
# 입력 : raw193.csv
# 출력 : mae - 0.2~112.0
# Size of IO, streamid, block_bio_queue, block_getrq, nvme_sq를 독립변수로 사용하고, block_rq_complete를 종속변수로 사용 함
# 데이터를 통해 먼저 네트워크를 생성하고 학습을 통해 예측한 데이터와 실제 데이터의 차이
# Dense layer에 relu를 사용하지 않을 때 오차가 적은 이유는 예측 값이 minus value를 가짐

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import models, layers, utils

def main():
	data = pd.read_csv("/home/mo/Project/BIO/raw_cassandra/raw193.csv")
	data = np.array(data)
	data = data[data[:,-1]!=0]		# when y = 0, row remove
	data = data[data[:,-3]!=0]

#	x_train = data[:2281675, 1:-1]
#	y_train = data[:2281675, -1]

#	x_test = data[2281675:, 1:-1]
#	y_test = data[2281675:, -1]

	x_train = data[:90000, 1:-1]
	y_train = data[:90000, -1]

	x_test = data[90000:100000, 1:-1]
	y_test = data[90000:100000, -1]

#	x_train = x_train.astype(np.float64)
	y_train = y_train.reshape(-1, 1)
#	x_test = x_test.astype(np.float32)
	y_test = y_test.reshape(-1, 1)
#	print(x_train.shape)
#	print("x_train\n",x_train)
#	print("Y_train\n",y_train)
#	print("x_test\n",x_test)
#	print("y_test\n",y_test)

	model = linear_model(x_train, y_train, x_test, y_test)

def linear_model(X, Y, X_test, Y_test):
	model = models.Sequential()
	model.add(layers.Dense(16, activation = 'relu', input_shape=(5,)))
	model.add(layers.Dense(32, activation = 'relu'))
	model.add(layers.Dense(64, activation = 'relu'))
	model.add(layers.Dense(128, activation = 'relu'))
#	model.add(layers.Dense(256, activation = 'relu'))
	model.add(layers.Dense(1,))

	model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
	model.fit(X, Y, epochs = 100, batch_size = 32)
	
	Y_pred = model.predict(X_test).astype(np.float64)
	print("Y_pred\n",Y_pred)
	print("Y_test\n",Y_test)

	error_mean = np.mean(np.abs(Y_test - Y_pred), axis=0)
	print('Error_mean:', error_mean)

	return model

main()
