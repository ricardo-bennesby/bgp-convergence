from pandas import DataFrame
from pandas import Series
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
#import numpy
import pandas as pd
import numpy as np
#import datetime
#import statistics
from numpy import median
from numpy import mean
from numpy import sum 
from datetime import datetime 
from collections import defaultdict
from collections import OrderedDict
from dateutil.parser import parse

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import model_from_json
from keras.models import Model
#import numpy
import pandas as pd
from keras import backend as K
from keras.backend import tf

from collections import Counter
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dropout

# specify columns to plot
groups = [0,1]
date = "01-09-2018"
FMT = '%H:%M:%S'
start_time = ['23:55:00','01:55:00','03:55:00','05:55:00','07:55:00','09:55:00','11:55:00','13:55:00','15:55:00','17:55:00','19:55:00','21:55:00']
base_time = ['00:00:00','02:00:00','04:00:00','06:00:00','08:00:00','10:00:00','12:00:00','14:00:00','16:00:00','18:00:00','20:00:00','22:00:00']

peers_list = ['45.61.0.85', '80.77.16.114', '98.159.46.1', '146.228.1.3', '165.254.255.2', '168.195.130.2', '176.12.110.8', '178.255.145.243', '185.193.84.191', '192.102.254.1', '193.0.0.56', '193.138.216.164', '193.150.22.1', '193.160.39.1', '195.47.235.100', '203.119.104.1', '203.123.48.6', '208.51.134.248', '212.25.27.44', '213.200.87.254','203.119.76.5','111.91.233.1','12.0.1.63','182.54.128.2','79.143.241.12','202.12.28.1'] 

#for peer_id in range(0,len(peers_list)):
#peer_id = 15
#list_peers = [0,2,3,6,7,10,11,12,13,14,15,16,17,18,19,20,22]
#list_peers = [0,2,3,6,7,10,12,13,14]
#list_peers = [0,2,3,6,7,9,10,12]
list_peers = [0,2,3,6,7,9,10,11,12,13,14,16,17,18,19]

list_peers = [0,6,7,9,10,13,14,18,19]

#list_peers = [0,6,7,10,13,14]
#list_peers = [0,7,10,13,14]
#list_peers = [4]
#to fix peers: 
#num_days = 97

#list_peers = [19]
num_events = 12
#num_days = 1
test_num_days = 1
seq_length = 300
num_features = 16
#num_epochs = 500
list_models = []

#WORKING FOR MONTH 6:
#list_peers = [0,2,3,6,7,10,11,12,13,14,15,16,17,18,19]
#to fix [day 15 for peer 12],  [day 19 for peer 14],  and  [day 28 for peer 19]:
#num_days = 27

#WORKING FOR MONTH 7:
#list_peers = [0,2,3,6,7,10,11,12,13,14,15,16,17,18,19,20,22]
#to fix peers: 4,9
#num_days = 31

#WORKING FOR MONTH 8:
#list_peers = [0,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19]
#num_days = 27

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

#day_list = ["01","03","04","05","06","07"]
#day_list = ["01","03","04","05","06","07","08","09","10","11","12","13","02"]
#day_list = ["01","03","04","05","06","07","09","10","11","13","02"]
#day_list = ["04-10","01-09","03-09","04-09","05-09","06-09","07-09","09-09","10-09","11-09","12-09","13-09","02-10"]
#day_list = ["01-09","03-09","04-09","05-09","06-09","07-09","09-09","10-09","11-09","13-09","02-10"]

#day_list = ["09-09","10-09","11-09","13-09","14-09","15-09","02-10","07-10"]
#day_list = ["01-09","03-09","04-09","05-09","06-09","07-09","08-09","09-09","10-09","11-09","13-09","14-09","15-09"]


#TEST 06:
#day_list = ["01-06","02-06","03-06","04-06","05-06","06-06","07-06","08-06","09-06","10-06","11-06","12-06","13-06","16-06","17-06","18-06","19-06","20-06","21-06","22-06","23-06","24-06","25-06","26-06","27-06","28-06","29-06","30-06","31-06"]

#TEST 07:
#day_list = ["05-07","06-07","07-07","08-07","09-07","10-07","11-07","12-07","13-07","16-07","17-07","18-07","19-07","20-07","21-07","22-07","23-07","24-07","25-07","26-07","27-07","28-07","29-07","30-07","31-07"]

#day_list = ["01-09","03-09","04-09","05-09","06-09","07-09","09-09","10-09","11-09","12-09","13-09","15-09","16-09","18-09","20-09","21-09","22-09","23-09","25-09","26-09","27-09","28-09","29-09","30-09"]
#TEST 09:
#day_list = ["01-09","03-09","04-09","05-09","06-09","07-09","09-09","10-09","11-09","13-09","15-09","16-09","18-09","20-09","22-09","23-09","24-09","25-09","26-09","27-09","28-09","30-09"]

#day_list = ["06-09"]
#day_list = ["01-09","03-09","04-09","05-09","06-09","07-09"]
day_list = ["02-10","07-10","09-10","13-10","14-10","15-10","16-10","17-10","20-10","21-10","22-10","23-10","24-10","25-10","26-10","27-10","31-10"]

#TEST 10
#day_list = ["02-10","04-10","07-10","09-10","10-10","11-10","13-10","14-10","15-10","16-10","17-10","18-10","20-10","21-10","22-10","23-10","24-10","25-10","26-10","27-10","28-10","29-10","30-10","31-10"]
#day_list = ["02-10","04-10","07-10","09-10","13-10","14-10","15-10","16-10","17-10","18-10","20-10","22-10","23-10","24-10","25-10","26-10","27-10","30-10","31-10"]


#TEST 08
#day_list = ["02-08","04-08","05-08","06-08","07-08","08-08","09-08","10-08","11-08","12-08","13-08","14-08","15-08","16-08","17-08","18-08","19-08","20-08","21-08","22-08","26-08","27-08","28-08","29-08","30-08","31-08"]
#day_list = ["02-08","04-08","05-08","06-08","07-08","08-08","09-08","11-08","12-08","13-08","14-08","15-08","16-08","17-08","18-08","19-08","20-08","21-08","22-08","26-08","31-08"]


prediction_ct_all = []
target_ct_all = []
filtered_pred_ct = [] # removed outiliers
filtered_target_ct = [] # removed outliers

ct_dict = defaultdict(list)

for day in day_list:
	print("\n############################################### TEST DATASET DAY " + str(day) + " ################################################")
	prediction_list = []
	target_list = []
	for peer_id_index in range(0,len(list_peers)):
		peer_id = list_peers[peer_id_index]
		#print("TEST PEER "+str(peer_id))
		print("PEER "+str(peers_list[peer_id]))
		test_dataset = read_csv('/home/ricardo/ripe/databases_updates/test-timestamps-'+day+"-"+peers_list[peer_id]+'.csv')
		test_values = test_dataset.values
		num_timestamps = (len(test_values))/((num_events*test_num_days))
		#print("num_timestamps:")
		#print(num_timestamps)

		test_dataset_y = read_csv('/home/ricardo/ripe/databases_updates/test-times_after-'+day+"-"+peers_list[peer_id]+'.csv')
		test_values_y = test_dataset_y.values

		#print("test-values_y:")
		#print(test_values_y)

		last_index = 0
		new_index = 0
		test_y_timestamps = []

		current_index_count = 1
		current_index_val = test_values_y[0][0]
		for dataset_size in range(0,test_num_days):
			event_announc = [1,3,5,7,9,11]
			previous_index = 1
			for index in range(new_index,len(test_values_y)):
				#print("values_y[index][0]:")
				#print(test_values_y[index][0]) 
				#print("-- current_index_count:")
				#print(current_index_count)

				if current_index_val != test_values_y[index][0]:
					current_index_count = 1
					current_index_val = test_values_y[index][0]

				if current_index_count < 3:
					if current_index_val != test_values_y[index][0]:
						current_index_count = 1
						current_index_val = test_values_y[index][0]
					else:
						current_index_count += 1

					if int(test_values_y[index][0]) in event_announc:
						#print("index: "+str(index))
						#print(values_y[index][1]) 
						test_y_timestamps.append(test_values_y[index][1])
						previous_index = int(test_values_y[index][0])
						del event_announc[0]
						#print("len: "+str(len(event_announc)))
						if len(event_announc) == 0:
							#print("index: "+str(index))
							#print(values_y[index][0])
							while(test_values_y[index][0]==11):
								index +=1
							new_index = index
							#print("new_index: "+str(new_index))
							#break
					elif len(test_y_timestamps) > 0:
						#print("len(y_timestamps):"+str(len(y_timestamps)))
						if len(event_announc)==0:
							if index+1 < len(test_values_y):
								if int(test_values_y[index][0])!= 12:
									test_y_timestamps.append(test_values_y[index][1])
								if int(test_values_y[index+1][0]) != 11:
									#new_index = index
									break	
						elif int(test_values_y[index][0]) == previous_index:
							test_y_timestamps.append(test_values_y[index][1])
						elif int(test_values_y[index][0]) > event_announc[0]: #for the case when no announcement was received at that index timestamp
							if test_values_y[index][0] == 12:
								last_timestamp_hour = int(test_y_timestamps[len(test_y_timestamps)-1].split(":")[0])
								if last_timestamp_hour != 20:
									#print(last_timestamp_hour)
									if last_timestamp_hour != 19:
										test_y_timestamps.append(base_time[event_announc[0]-1])
										#print("event_announc[0]: "+str(event_announc[0]))
										del event_announc[0]
									new_index = index
							else:
								test_y_timestamps.append(base_time[event_announc[0]-1])
								#print("event_announc[0]: "+str(event_announc[0]))
								del event_announc[0]	
					else:
						#print()
						test_y_timestamps.append(base_time[index])
						del event_announc[0]
						#print("event_announc:")
						#print(event_announc)
						#index +=1
						new_index = index
				else:
					if current_index_val == test_values_y[index][0]:
						current_index_count += 1

		#print("test_y_timestamps:")
		#print(test_y_timestamps)

		test_new_y_timestamps = []
		len_y_sequences = 3
		current_sequence_index = 1
		#print("test_new_y_timestamps:")
		test_new_y_timestamps.append(test_y_timestamps[0])
		for y_index in range(1,len(test_y_timestamps)):
			#print("y_index:"+str(y_index))
			if current_sequence_index <= len_y_sequences:
				if test_y_timestamps[y_index].split(":")[0] == test_new_y_timestamps[len(test_new_y_timestamps)-1].split(":")[0] or int(test_y_timestamps[y_index].split(":")[0]) == int(test_new_y_timestamps[len(test_new_y_timestamps)-1].split(":")[0])+1:
					test_new_y_timestamps.append(test_y_timestamps[y_index])
					test_timestamp_y = test_y_timestamps[y_index].split(":")[0]
					#print(y_timestamps[y_index])
					#print(int(test_timestamp_y))
					current_sequence_index+=1
				else:
					while current_sequence_index < len_y_sequences:
						repeated_sequence = 1
						test_new_y_timestamps.append(test_new_y_timestamps[len(test_new_y_timestamps)-1]) #append the last element of the lost to the same list
						current_sequence_index+=1	
					test_new_y_timestamps.append(test_y_timestamps[y_index])
					current_sequence_index = 1
			else:
				#print("-- New event --")
				#print("y_index:"+str(y_index))
				#timestamp_y = y_timestamps[y_index].split(":")[0]
				#current_sequence_index = 1
				test_new_y_timestamps.append(test_y_timestamps[y_index])
				current_sequence_index+=1

		while current_sequence_index < len_y_sequences:
			test_new_y_timestamps.append(test_new_y_timestamps[len(test_new_y_timestamps)-1]) #append the last element of the lost to the same list
			current_sequence_index+=1

		#print("len new_y_timestamps:")
		#print(len(test_new_y_timestamps))

		#print("new_y_timestamps:")
		#print(test_new_y_timestamps)

		#print("*** Event 1 ***")
		event_num = 2
		cont = 1
		for index in range(0,len(test_new_y_timestamps)):
			#print(test_new_y_timestamps[index])
			if cont >= 6:
				#print("*** Event "+str(event_num)+" ***")
				#print(new_y_timestamps[index])
				event_num+=1
				cont = 0
			cont+=1

		if len(test_y_timestamps) == 0:
			print("No test announcements events for peer " + peers_list[peer_id])
			exit()

		test_list = []
		for num_event in range(0,num_events*test_num_days):
			start_index = num_event * num_timestamps
			#print("start_index: "+str(start_index))
			#print(" ---- Event " + str(num_events*num_days) + "----- ")
			#print(values[start_index:start_index+num_timestamps,])
			test_list.append(test_values[start_index:start_index+num_timestamps])

		#print("test_list:")
		#print(test_list)

		#print(test_list[2][0])
		#print("training_list:")
		test_x = []
		last_index = 0
		for x in range(0,test_num_days):
			current_index = last_index
			last_index = current_index
			for i in [0,2,4,6,8,10]:
				#print("i:"+str(i+last_index))
				current_index = last_index + i
				#print("current_index:")
				test_features = []
				for test_list_len in range(0,len(test_list[i+last_index])):
					#print(training_list[i+last_index][training_list_len][0])
					if datetime.strptime(test_list[i+last_index][test_list_len][0], FMT) < datetime.strptime(start_time[i], FMT):
						#print("Next day")
						tdelta = datetime.strptime(test_list[i+last_index][test_list_len][0], FMT) - datetime.strptime(start_time[i], FMT)
						#tdelta = tdelta.split(",")
						#tdelta = tdelta[1]
						#tdelta = tdelta.split(" ")[1]
						#print(tdelta.seconds)
						#print(str(tdelta.seconds)+" - "+str(test_list[i+last_index][test_list_len][1]))
						test_features.append(tdelta.seconds)
						test_features.append(test_list[i+last_index][test_list_len][1])
						test_features.append(test_list[i+last_index][test_list_len][2])
						test_features.append(test_list[i+last_index][test_list_len][3])
						test_features.append(test_list[i+last_index][test_list_len][4])
						test_features.append(test_list[i+last_index][test_list_len][5])
						test_features.append(test_list[i+last_index][test_list_len][6])
						test_features.append(test_list[i+last_index][test_list_len][7])
						test_features.append(test_list[i+last_index][test_list_len][8])
						test_features.append(test_list[i+last_index][test_list_len][9])
						test_features.append(test_list[i+last_index][test_list_len][10])
						test_features.append(test_list[i+last_index][test_list_len][11])
						test_features.append(test_list[i+last_index][test_list_len][12])
						test_features.append(test_list[i+last_index][test_list_len][13])
						test_features.append(test_list[i+last_index][test_list_len][14])
						test_features.append(test_list[i+last_index][test_list_len][15])
					else:
						tdelta = datetime.strptime(test_list[i+last_index][test_list_len][0], FMT) - datetime.strptime(start_time[i], FMT)
						#print(str(tdelta.seconds)+" - "+str(test_list[i+last_index][test_list_len][1]))
						test_features.append(tdelta.seconds)
						test_features.append(test_list[i+last_index][test_list_len][1])
						test_features.append(test_list[i+last_index][test_list_len][2])
						test_features.append(test_list[i+last_index][test_list_len][3])
						test_features.append(test_list[i+last_index][test_list_len][4])
						test_features.append(test_list[i+last_index][test_list_len][5])
						test_features.append(test_list[i+last_index][test_list_len][6])
						test_features.append(test_list[i+last_index][test_list_len][7])
						test_features.append(test_list[i+last_index][test_list_len][8])
						test_features.append(test_list[i+last_index][test_list_len][9])
						test_features.append(test_list[i+last_index][test_list_len][10])
						test_features.append(test_list[i+last_index][test_list_len][11])
						test_features.append(test_list[i+last_index][test_list_len][12])
						test_features.append(test_list[i+last_index][test_list_len][13])
						test_features.append(test_list[i+last_index][test_list_len][14])
						test_features.append(test_list[i+last_index][test_list_len][15])
				test_x.append(test_features)
			last_index = current_index + 2
			#print("last_index:" + str(last_index))
			if last_index >= len(test_list):
				break

		test_y = []
		#print("Y values:")
		#print("test_new_y_timestamps: "+str(len(test_new_y_timestamps)))
		#print(test_new_y_timestamps)
		last_index = 0
		#last_index2 = 0
		test_y_lists = []
		for x in range(0,test_num_days):
			current_index = last_index
			last_index = current_index
			for j in range(0,len(base_time)/2):
				#print("j*2: "+str(j*2))
				#print("j+last_index: "+str(j+last_index))
				test_y_instance_list = []
				#current_index = last_index + j
				#current_index2 = last_index2
				#last_index2 = current_index2
				for num_array in range(0,len_y_sequences):
					current_index = last_index + num_array  
					if datetime.strptime(test_new_y_timestamps[num_array+last_index], FMT) < datetime.strptime(base_time[j*2], FMT):
						#print("test_new_y_timestamps[j+last_index+num_array]: "+str(test_new_y_timestamps[num_array+last_index]))
						#print("start_time[j*2]): "+str(start_time[j*2]))
						tdelta = datetime.strptime(test_new_y_timestamps[num_array+last_index], FMT) - datetime.strptime(base_time[j*2], FMT)
						test_y.append(tdelta.seconds)
						test_y_instance_list.append(tdelta.seconds)
					else:
						#print("test_new_y_timestamps[j+last_index+num_array]: "+str(test_new_y_timestamps[num_array+last_index]))
						#print("start_time[j*2]): "+str(start_time[j*2]))
						tdelta = datetime.strptime(test_new_y_timestamps[num_array+last_index], FMT) - datetime.strptime(base_time[j*2], FMT)
						test_y.append(tdelta.seconds)
						test_y_instance_list.append(tdelta.seconds)
						#last_index2 = current_index2 + 1
				last_index = current_index + 1 
				test_y_lists.append(test_y_instance_list)

		#print((training_x))
		#print("test_y:")
		#print(test_y)

		test_values_y = np.array(test_y).reshape(-1,1) # transform valuesY to array
		scalerY = MinMaxScaler(feature_range=(0, 1))
		scaledY = scalerY.fit_transform(test_values_y)

		len_values_y = int(len(test_values_y)/len_y_sequences)
		scaledY = np.reshape(scaledY, (len_values_y,len_y_sequences))
		#scaledY = np.reshape(scaledY, (len(test_values_y)/6,6))
		#print(scaledY.shape)

		#print(test_values_y)
		#print(scaledY)

		scalerX = MinMaxScaler(feature_range=(0, 1))
		scaledX = scalerX.fit_transform(test_x)

		# convert list of lists to array and pad sequences if needed
		#test_X = pad_sequences(test_x, maxlen=seq_length, dtype='float32')
		#print(test_X.shape)

		# reshape X to be [samples, time steps, features]
		#scaledX = np.reshape(training_x, (scaledX.shape[0], seq_length, 2))
		test_X = np.reshape(scaledX, (len(test_x), seq_length, num_features))

		# load json and create model
		'''
		json_file = open('model.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		model_file_name = "model-"+str(list_peers[peer_id_index])+str(".json")
		print("model_file_name:")
		print(model_file_name)
		model = model_from_json(model_file_name)'''

		# create and fit the model
		model = Sequential()
		model.add(LSTM(16, input_shape=(test_X.shape[1], test_X.shape[2])))
		model.add(Dropout(0.2))
		#model.add(Dense(16, activation='relu'))
		#model.add(LSTM(32, input_shape=(test_X.shape[1], test_X.shape[2])))
		#model.add(Dropout(0.1))
		#model.add(LSTM(24, input_shape=(test_X.shape[1], test_X.shape[2])))
		#model.add(Dense(scaledY.shape[1], activation='sigmoid'))
		model.add(Dense(6, activation='relu'))
		#model.add(Dropout(0.1))
		#model.add(Dense(6, activation='relu'))
		model.add(Dense(scaledY.shape[1], activation='relu'))
		#model.add(Dense(3, activation='relu'))
		#model.compile(loss='mae', optimizer='adam')

		model.compile(loss='mae', optimizer='adam')

		# load weights into new model
		model_weights_name = 'lstm5_model-'+str(list_peers[peer_id_index])+'.h5'
		model.load_weights(model_weights_name)
		#print("Loaded model from disk")

		#print("peer_id_index: "+str(peer_id_index))
		#print("len list_models: "+str(len(list_models)))

		prediction = model.predict(test_X, verbose=0)
		inv_yhat = scalerY.inverse_transform(prediction)
		prediction_list.append(inv_yhat)
		#inv_yhat = inv_yhat[:,0]

		#print("prediction:")
		#print(prediction)

		#print("inv_yhat:")
		#print(inv_yhat)

		inv_y = scalerY.inverse_transform(scaledY)
		target_list.append(inv_y)

		#print("\n")
		#print "|  Predicted        -------       Real       "
		pred_len = len(prediction)
		#print("pred_len: "+str(pred_len))

		#print("len(inv_yhat[iterator].tolist()):")
		#print(len(inv_yhat[0].tolist()))

		#print("inv_yhat[iterator].tolist():")
		#print(inv_yhat[0].tolist())

		#print("inv_y[iterator].tolist():")
		#print(inv_y[0].tolist())

		
		#print("Prediction for peer: "+str(peer_id))
		iterator = 0
		while iterator < pred_len:
			#print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator],inv_y[iterator]) )
			#print(inv_yhat[iterator].tolist(),inv_y[iterator].tolist())
			#print("|  PREDICTED       -------       TARGET")
			#for predict_item in range(0,len(inv_yhat[iterator].tolist())):
			#	print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator].tolist()[predict_item],inv_y[iterator].tolist()[predict_item]) )	
			#print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator],inv_y[iterator]) )
			iterator += 1
		'''rmse_val = rmse(np.array(prediction_list), np.array(target_list))
		print("RMSE: " + str(rmse_val))'''

	#print("Prediction list:")
	#print(prediction_list)

	'''
	for peer_index in range(0,len(prediction_list)):
		print("Peer ID: "+str(peer_index))
		print(prediction_list[peer_index])'''
	print("...............................................................")

	prediction_event = []
	target_event = []
	prediction_ct = []
	target_ct = []
	avg_daily_rmse = []
	avg_rmse_ct = []
	mape_sum_day = 0.0

	for num_event in range(0,num_events/2):
		ct_list = []
		#print("\n")
		#print("Convergence Time lists for event: "+str(num_event))
		for peer_index in range(0,len(prediction_list)):
			#print("Peer ID: "+str(peer_index))
			#print(prediction_list[peer_index][num_event])
			for ct in range(0,len(prediction_list[peer_index][num_event])):
				#if int(prediction_list[peer_index][num_event][ct]) != 0:
				ct_list.append(int(prediction_list[peer_index][num_event][ct]))
				prediction_event.append(int(prediction_list[peer_index][num_event][ct]))
		print("predicted_list:")
		print(ct_list)
		if len(ct_list) > 0:
			max_timestamp =  max(ct_list)
			min_timestamp =  min(ct_list)
			#convergence_time = max_timestamp - min_timestamp
			convergence_time = max_timestamp
			#print("Predicted max_timestamp: "+str(max_timestamp))
			#print("Predicted min_timestamp: "+str(min_timestamp))
			print("** Predicted Convergence Time: "+str(convergence_time))
			prediction_ct.append(max_timestamp)
			prediction_ct_all.append(max_timestamp)
		else:
			print("** Predicted Convergence Time: 0")
			prediction_ct.append(0)
			prediction_ct_all.append(0)

		t_list = []
		#print("\n")
		#print("Target Convergence Time lists for event: "+str(num_event))
		for peer_index in range(0,len(target_list)):
			#print("Peer ID: "+str(peer_index))
			#print(target_list[peer_index][num_event])
			for ct in range(0,len(target_list[peer_index][num_event])):
				#if int(target_list[peer_index][num_event][ct]) != 0:
				t_list.append(int(target_list[peer_index][num_event][ct]))
				target_event.append(int(target_list[peer_index][num_event][ct]))
		print("target_list:")
		print(t_list)
		if len(t_list) > 0:
			max_timestamp =  max(t_list)
			min_timestamp =  min(t_list)
			#convergence_time = max_timestamp - min_timestamp
			convergence_time = max_timestamp
			#print("Target max_timestamp: "+str(max_timestamp))
			#print("Target min_timestamp: "+str(min_timestamp))
			print("** Target Convergence Time: "+str(convergence_time))
			target_ct.append(max_timestamp)
			target_ct_all.append(max_timestamp)
		else:
			print("** Target Convergence Time: 0")
			target_ct.append(0)

		#print("target event convergence: "+str(target_ct_all[len(target_ct_all)-1]))
		#print("predicted event convergence: "+str(prediction_ct_all[len(prediction_ct_all)-1]))

		ct_diff = int(abs(target_ct_all[len(target_ct_all)-1] - prediction_ct_all[len(prediction_ct_all)-1]))
		if ct_diff <= 90:
			filtered_target_ct.append(target_ct_all[len(target_ct_all)-1])
			filtered_pred_ct.append(prediction_ct_all[len(prediction_ct_all)-1])

		rmse_val = rmse(np.array(ct_list), np.array(t_list))
		avg_daily_rmse.append(rmse_val)
		print("Event " + str(num_event) + " - RMSE:" + str(rmse_val))
		rmse_ct = rmse(np.array(prediction_ct), np.array(target_ct))
		avg_rmse_ct.append(rmse_ct)
		#mape_sum_day += float(abs((sorted_target_ct[ct_index] - sorted_predicted_ct[ct_index])))/float(sorted_target_ct[ct_index])
		print("Event " + str(num_event) + " - Convergence Time RMSE:" + str(avg_rmse_ct))
		print("...............................................................")
		#for ct_index in range(0,len(ct_list)):
		#	mape_sum_day += float(abs((t_list[ct_index] - ct_list[ct_index])))/float(t_list[ct_index])
		#mape_day = float(mape_sum_day)/float(len(t_list))
		#print("MAPE day: "+str(mape_day))

	print("Average RMSE: " + str(mean(avg_daily_rmse)))
	print("Convergence Time RMSE: " + str(mean(avg_rmse_ct)))
	print("******************************************************************")

	#prediction_sorted = sorted(prediction_event)
	#target_sorted = sorted(target_event)

	#print("ordered lists:")
	#print(sorted(prediction_event))
	#print(sorted(target_event))

	pyplot.plot(prediction_event, label='prediction')
	pyplot.plot(target_event, label='target')
	pyplot.legend()
	pyplot.savefig('prediction-target-'+str(day)+'.png')
	pyplot.clf()
	pyplot.cla()
	pyplot.close()

	pyplot.plot(prediction_ct, label='pred ct')
	pyplot.plot(target_ct, label='target ct')
	pyplot.legend()
	pyplot.savefig('conv_time-prediction-target-'+str(day)+'.png')
	pyplot.clf()
	pyplot.cla()
	pyplot.close()

#pyplot.figure(figsize=(16,4))
#pyplot.plot(prediction_ct_all, label='pred ct', color='red')
#pyplot.plot(prediction_ct_all, 'ro')
#pyplot.plot(target_ct_all, label='target ct', color='blue')
#pyplot.plot(target_ct_all, 'bo')

'''
pyplot.figure(figsize=(16,4))
pyplot.plot(filtered_pred_ct, label='pred ct', color='red')
pyplot.plot(filtered_pred_ct, 'ro')
pyplot.legend()
pyplot.grid(True)
pyplot.savefig('final_conv_time-prediction'+str(day)+'.png')
pyplot.clf()
pyplot.cla()
pyplot.close()


pyplot.figure(figsize=(16,4))
pyplot.plot(filtered_target_ct, label='target ct', color='blue')
pyplot.plot(filtered_target_ct, 'bo')
pyplot.legend()
pyplot.grid(True)
pyplot.savefig('final_conv_time-target'+str(day)+'.png')
pyplot.clf()
pyplot.cla()
pyplot.close()
'''

pyplot.figure(figsize=(16,4))
pyplot.plot(filtered_pred_ct, label='pred ct', color='red')
pyplot.plot(filtered_pred_ct, 'r^')
pyplot.plot(filtered_target_ct, label='target ct', color='blue')
pyplot.plot(filtered_target_ct, 'bo')
pyplot.legend()
pyplot.grid(True)
pyplot.savefig('final_conv_time-prediction-target-'+str(day)+'.png')
pyplot.clf()
pyplot.cla()
pyplot.close()

for i in range(0,len(target_ct_all)):
	ct_dict[target_ct_all[i]].append(prediction_ct_all[i]) 

sorted_ct_dict = OrderedDict(sorted(ct_dict.items()))

#print("sorted_ct_dict:")
#print(sorted_ct_dict)

sorted_predicted_ct = []
sorted_target_ct = []
num_outliers = 0

for item in sorted_ct_dict.keys():
	for index in range(0,len(sorted_ct_dict[item])): 
		ct_diff = int(abs(item-sorted_ct_dict[item][index]))
		if ct_diff > 90:
			print("Outlier target: "+str(ct_diff))
			num_outliers += 1
		else:
			sorted_target_ct.append(item)
			sorted_predicted_ct.append(sorted_ct_dict[item][index])


mape_sum = 0.0
#num_outliers = 0
for ct_index in range(0,len(sorted_target_ct)):
	#abs_test = abs((sorted_target_ct[ct_index] - sorted_predicted_ct[ct_index]))
	#print("abs_test: "+str(abs_test))
	#partial_div = float(abs_test)/float(sorted_target_ct[ct_index])
	#print("partial_div: "+str(partial_div))
	'''ct_diff = int(abs((sorted_target_ct[ct_index] - sorted_predicted_ct[ct_index])))
	if ct_diff > 90:
		print("Outlier target: "+str(ct_diff))
		num_outliers += 1
	else:'''
	mape_sum += float(abs((sorted_target_ct[ct_index] - sorted_predicted_ct[ct_index])))/float(sorted_target_ct[ct_index])
	#print("sorted_target_ct[ct_index]: "+str(sorted_target_ct[ct_index]))
	#print("sorted_predicted_ct[ct_index]: "+str(sorted_predicted_ct[ct_index]))
	#print("mape_sum: "+str(mape_sum))
mape = float(mape_sum)/float(len(sorted_target_ct)-num_outliers)
print("MAPE: "+str(mape))

print("len(sorted_target_ct):"+str(len(sorted_target_ct)))

print("percentage of outliers: "+str(float(num_outliers)/float(len(sorted_target_ct))*100 )+str("%"))

pyplot.plot(sorted_predicted_ct, label='predicted conv. time', color='red')
pyplot.plot(sorted_predicted_ct, 'ro')
pyplot.plot(sorted_target_ct, label='target conv. time', color='blue')
pyplot.plot(sorted_target_ct, 'bo')
pyplot.legend()
pyplot.grid(True)
pyplot.savefig('sorted_conv_time-prediction-target-ordered.png')
pyplot.clf()
pyplot.cla()
pyplot.close()

print("sorted_predicted_ct:")
print(sorted_predicted_ct)
print("sorted_target_ct:")
print(sorted_target_ct)


#------------------------------------------------------------------------------------
