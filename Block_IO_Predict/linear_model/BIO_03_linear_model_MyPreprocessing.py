'''
작성일 : 2020-09-10
작성자 : 정성모
코드 개요 :
    Size of IO, streamid, block_bio_queue, block_getrq, nvme_sq를 독립변수로 사용하고,
	block_rq_complete를 종속변수로 사용 함. 각 독립변수의 최솟값을 원 데이터에서 뺀 데이터를 학습데이터로 사용
결과 : mae - 0.3
'''

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

	# 전처리 - 각 컬럼의 가장 작은 값을 데이터에 빼주어 학습 데이터로 사용
	data_min = np.min(data, axis=0)
#	print(data_min[-4:-1])
	data_min[0] = 0
	data_min[1] = 0
	data_min = data_min
	print(data_min)
	data = data - data_min
	print(data)

	x_train = data[:2700000, 1:-1]
	y_train = data[:2700000, -1]

	x_test = data[2700000:-1, 1:-1]
	y_test = data[2700000:-1, -1]
	y_testReal = y_testReal.reshape(-1, 1)

	y_train = y_train.reshape(-1, 1)
	y_test = y_test.reshape(-1, 1)

	model = linear_model(x_train, y_train)
	
	# mae를 이용하여 데이터 차이 확인
	y_pred = model.predict(x_test).astype(np.float64)
	y_pred = y_pred + data_min[-1]
	print("Y_pred\n",y_pred)
	print("Y_test\n",y_testReal)
	
	error_mean = np.mean(np.abs(y_testReal - y_pred), axis=0)
	print('Error_mean:', error_mean)

# linear model 생성
def linear_model(X, Y):
	model = models.Sequential()
	model.add(layers.Dense(16, input_shape=(5,)))
	model.add(layers.Dense(32))
	model.add(layers.Dense(64))
	model.add(layers.Dense(128))
	model.add(layers.Dense(1,))

	model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
	model.fit(X, Y, epochs = 10, batch_size = 32)

	return model

main()
