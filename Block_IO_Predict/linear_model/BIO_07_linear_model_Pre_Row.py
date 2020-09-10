'''
작성일 : 2020-09-10
작성자 : 정성모
코드 개요 :
    block_bio_queue, block_getrq, nvme_sq, block_rq_complete을 상대시간으로 변경
	BIO 사이클의 3개의 이벤트 데이터, Sector, 전의 row 데이터들을 이용하여(5, 8, 10개 rows) RG_COMPLETE 데이터 예측
결과 : mae = 0.05~0.08
'''

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import models, layers, utils
from sklearn.preprocessing import MinMaxScaler

def main():
	data = pd.read_csv("/home/mo/Project/BIO/raw_cassandra/raw193.csv")
	data = data.copy()
	data = data[data['block_rq_complete']!=0]
	data = data[data['block_getrq']!=0]
	data = data[data['Sector']!=0]
	data.pop('Size of IO')
	data.pop('streamid')

	data = data.reset_index()
	data.pop('index')
	
	# Convert absolute time to relative time
	data['block_rq_complete']= data['block_rq_complete'] - data['nvme_sq']
	data['nvme_sq']= data['nvme_sq'] - data['block_getrq']
	data['block_getrq']= data['block_getrq'] - data['block_bio_queue']
	bio_queue_preprocessing(data)

	# pre rows + data
	rows = 5
	tail = pre_rows(data, rows)
	tail = pd.DataFrame(tail)
	data = pd.concat([tail, data],axis=1)

	# Dividing data into train and test
	train_data = data.sample(frac=0.8,random_state=0)
	test_data = data.drop(train_data.index)

	# Extract label	
#	train_label = train_data.pop("block_rq_complete")
#	test_label = test_data.pop("block_rq_complete")

	# dataset 1) standardization + normalization
	sd_train_data = standardization(train_data)
	norm_train_data = normalization(sd_train_data)
	sd_test_data = standardization(test_data)
	norm_test_data = normalization(sd_test_data)

	# Matching labels and variables, After normalization
#	train_label = train_label[norm_train_data.index]
#	test_label = test_label[norm_test_data.index]

	# normalization Extract label
	train_label = norm_train_data.pop("block_rq_complete")
	test_label = norm_test_data.pop("block_rq_complete")

	# dataset 2) normalization
#	norm_train_data = normalization(train_data)
#	norm_test_data = normalization(test_data)
#	scaler = MinMaxScaler()
#	norm_train_data = scaler.fit_transform(train_data[:])
#	norm_test_data = scaler.fit_transform(test_data[:])

	norm_train_data = np.array(norm_train_data)
	train_label = np.array(train_label).reshape(-1,1)
	norm_test_data = np.array(norm_test_data)
	test_label = np.array(test_label).reshape(-1,1)

#	print("x_train\n",norm_train_data)
#	print("Y_train\n",train_label.shape)
#	print("x_test\n",norm_test_data)
#	print("y_test\n",test_label.shape)

	model = linear_model(norm_train_data, train_label, norm_test_data, test_label, rows*5+4)
	
# input : pandas.DataFrame, 이전 row의 갯수
def pre_rows(x, rows):
	'''
	함수 개요 :
	    현재 row 기준으로 정해진 이전 row들의 값들을 컬럼으로 추가
        ex) rows 가 5 인 경우, 현재 row-5번째까지의 값들(sector, bio_queue, ... )을 각 컬럼으로 추가 ※ 최종 컬럼의 갯수는 rows*5+4 = 29개
	파라미터 :
        x = pandas DataFrame 형태의 원 데이터
		rows = 이전 row 데이터들 갯수
	'''
	data = np.array(x)
	temp_total = np.empty((len(data),rows*5))
	for i in range(len(data)):
		temp = np.array([])
		for j in range(1,rows+1):
			temp = np.append(temp,data[i-j,:])
		temp_total[i] = temp
	for i in range(rows):
		temp_total[i,i*5:rows*5] = 0
	return temp_total
	
def bio_queue_preprocessing(x):
	'''
	함수 개요 :
	    bio_queue의 해당 row의 값은 해당 row값에서 첫번째 row 값에서 뺀 값, 첫번째 row 값은 0
	파라미터 :
        x = pandas DataFrame 형태의 원 데이터
	'''
	data = np.array(x['block_bio_queue'])
	temp = np.zeros(len(data))
	for i in range(len(data)):
		temp[i] = data[i] - data[0]
	temp[0] = 0.
	x['block_bio_queue'] = temp
	
	return x

# info
# -2 > x or 2 < x, train_data 300000
def standardization(x):
	'''
	함수 개요 : Data 표준화
	파라미터 :
        x = pandas DataFrame 형태의 원 데이터
	'''
	x = (x - np.mean(x,axis=0)) / np.std(x,axis=0)
	x = x[x[:]<=2]
	x = x[x[:]>=-2]
	x = x.dropna(axis=0)
#	ls = x.index.values.tolist()
#	print(len(x))
#	print(np.min(x,axis=0))

	return x



def normalization(x):
	'''
	함수 개요 : Data 정규화
	파라미터 :
        x = pandas DataFrame 형태의 원 데이터
	'''
	x = (x - np.min(x,axis=0)) / (np.max(x,axis=0) - np.min(x,axis=0))
	x = x.dropna(axis=0)
	return x



def linear_model(X, Y, X_test, Y_test, rows):

	init = tf.keras.initializers.he_normal()

	model = models.Sequential()
	model.add(layers.Dense(16, activation = 'relu', kernel_initializer=init, input_shape=(rows,)))
	model.add(layers.Dense(1, activation = 'relu'))
	model.add(layers.Dense(1))

	model.compile(loss='mae', optimizer='adam')
	model.fit(X, Y, epochs = 10, batch_size = 4096)
	
	Y_pred = model.predict(X_test)
	print("Y_pred\n",Y_pred)
	print("Y_test\n",Y_test)
	print("minuse value : ",len(Y_pred[Y_pred < 0]))
	print("0 value : ", len(Y_pred[Y_pred==0]))

	error_mean = np.mean(np.abs(Y_test - Y_pred), axis=0)
	print('Error_mean:', error_mean)

	w1 = model.layers[0].get_weights()[0]
	b1 = model.layers[0].get_weights()[1]
	w2 = model.layers[1].get_weights()[0]
	b2 = model.layers[1].get_weights()[1]
	
	print(w1)
	print(b1)
	print(w2)
	print(b2)

	return model


main()
