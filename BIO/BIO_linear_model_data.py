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

main()
