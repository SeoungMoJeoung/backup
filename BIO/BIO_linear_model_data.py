import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import models, layers, utils

def main():
	data = pd.read_csv("/home/mo/Project/BIO/raw_cassandra/raw193.csv")
	data = data.copy()
#	data = data[data['block_rq_complete']!=0]
#	data = data[data['block_getrq']!=0]
#	data = data[data['Sector']!=0]
	data.pop('Size of IO')
	data.pop('streamid')

#	data = data.loc[0:99]
	print(data)

#	data.to_csv("Original_data.csv", mode='w',index=False)
	
	# coefficient
#	co = data.corr()
#	print("original data\n",co)
	
	# Convert absolute time to relative time
	data['block_rq_complete']= data['block_rq_complete'] - data['nvme_sq']
	data['nvme_sq']= data['nvme_sq'] - data['block_getrq']
	data['block_getrq']= data['block_getrq'] - data['block_bio_queue']
	bio_queue_preprocessing(data)
#	print()
#	timeco = data.corr()
#	print("relative time\n",timeco)
	
	print(data)


#	data.to_csv("relative_data.csv", mode='w')

	# Dividing data into train and test
	train_data = data.sample(frac=0.8,random_state=0)
	test_data = data.drop(train_data.index)


	# Extract label	
#	train_label = train_data.pop("block_rq_complete")
#	test_label = test_data.pop("block_rq_complete")

#	print(train_data)

	sd_train_data = standardization(train_data)
	norm_train_data = normalization(sd_train_data)

	sd_test_data = standardization(test_data)
	norm_test_data = normalization(sd_test_data)


#	norm_train_data = norm_train_data[norm_train_data[:]<0]
#	norm_train_data = norm_train_data.dropna()
#	print(len(norm_train_data))

#	norm_test_data = norm_test_data[norm_test_data[:]<0]
#	norm_test_data = norm_test_data.dropna()
#	print(len(norm_test_data))

#	norm_train_data = normalization(train_data)
#	norm_test_data = normalization(test_data)

#	norm_train_data = np.array(norm_train_data)
#	train_label = np.array(train_label).reshape(-1,1)
#	norm_test_data = np.array(norm_test_data)
#	test_label = np.array(test_label).reshape(-1,1)
#	print()
#	ptrainco = norm_train_data.corr()
#	print("train\n",ptrainco)
#	print()
#	ptestco = norm_test_data.corr()
#	print("test\n",ptestco)

#	print("x_train\n",norm_train_data.shape)
#	print("Y_train\n",train_label.shape)
#	print("x_test\n",norm_test_data.shape)
#	print("y_test\n",test_label.shape)

#	model = linear_model(norm_train_data, train_label, norm_test_data, test_label)


def bio_queue_preprocessing(x):

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
	x = (x - np.mean(x,axis=0)) / np.std(x,axis=0)
#	x = x[x[:]<=2]
#	x = x[x[:]>=-2]
	x = x.dropna(axis=0)
#	print(len(x))
#	print(np.min(x,axis=0))
	return x


def normalization(x):
	x = (x - np.min(x,axis=0)) / (np.max(x,axis=0) - np.min(x,axis=0))
	x = x.dropna(axis=0)
	return x



def linear_model(X, Y, X_test, Y_test):
	model = models.Sequential()
	model.add(layers.Dense(16, input_shape=(4,)))
#	model.add(layers.Dense(32))
#	model.add(layers.Dense(64))
#	model.add(layers.Dense(128))
	model.add(layers.Dense(1,))

	model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
	model.fit(X, Y, epochs = 100, batch_size = 32)
	
	Y_pred = model.predict(X_test)
	print("Y_pred\n",Y_pred)
	print("Y_test\n",Y_test)

	error_mean = np.mean(np.abs(Y_test - Y_pred), axis=0)
	print('Error_mean:', error_mean)

	return model


main()
