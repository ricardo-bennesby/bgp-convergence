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

#list_peers = [0,2,6,7,9,10,13,14,16]
list_peers = [0,2,3,6,7,9,10,11,12,13,14,16,17,18,19]
list_peers = [0,6,7,9,10,13,14,18,19]

num_days = 95
num_days = 103
num_days = 98

num_events = 12
test_num_days = 1
seq_length = 300
num_features = 16
num_epochs = 500
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

for peer_id_index in range(0,len(list_peers)):
	peer_id = list_peers[peer_id_index]
	y_timestamps = []
	print("TRAINING PEER "+str(peer_id))
	print("TRAINING PEER "+str(peers_list[peer_id]))
	dataset = read_csv('../datasets/timestamps-'+peers_list[peer_id]+'.csv')

	values = dataset.values
	print("len(values):")
	print(len(values))
	if len(values) == 0:
		break
	num_timestamps = (len(values))/((num_events*num_days))
	print("num_timestamps:")
	print(num_timestamps)

	dataset_y = read_csv('../datasets/times_after-'+peers_list[peer_id]+'.csv')

	values_y = dataset_y.values

	last_index = 0
	new_index = 0
	current_index_count = 1
	current_index_val = values_y[0][0]
	for dataset_size in range(0,num_days):
		event_announc = [1,3,5,7,9,11]
		previous_index = 1
		for index in range(new_index,len(values_y)):
			if current_index_val != values_y[index][0]:
				current_index_count = 1
				current_index_val = values_y[index][0]

			if current_index_count < 3:
				if current_index_val != values_y[index][0]:
					current_index_count = 1
					current_index_val = values_y[index][0]
				else:
					current_index_count += 1

				if int(values_y[index][0]) in event_announc:
					#if current_index_count < 3:  
						#if current_index_val == values_y[index][0]:
							#print("index: "+str(index))
					y_timestamps.append(values_y[index][1])
					previous_index = int(values_y[index][0])
					del event_announc[0]
					#print("len: "+str(len(event_announc)))
					if len(event_announc) == 0:
						#print("index: "+str(index))
						#print(values_y[index][0])
						while(values_y[index][0]==11):
							index +=1
						new_index = index
						#print("new_index: "+str(new_index))
						#current_index_count += 1
						#break
				elif len(y_timestamps) > 0:
					#print("len(y_timestamps):"+str(len(y_timestamps)))
					if len(event_announc)==0:
						if index+1 < len(values_y):
							if int(values_y[index][0])!= 12:
								#print("current_index_count:")
								#print(current_index_count)
								y_timestamps.append(values_y[index][1])
							if int(values_y[index+1][0]) != 11:
								#new_index = index
								break	
					elif int(values_y[index][0]) == previous_index:
						y_timestamps.append(values_y[index][1])
					elif int(values_y[index][0]) > event_announc[0]: #for the case when no announcement was received at that index timestamp
						if values_y[index][0] == 12:
							last_timestamp_hour = int(y_timestamps[len(y_timestamps)-1].split(":")[0])
							if last_timestamp_hour != 20:
								if last_timestamp_hour != 19:
									y_timestamps.append(base_time[event_announc[0]-1])
									#print("event_announc[0]: "+str(event_announc[0]))
									del event_announc[0]
								new_index = index
								#break	
						else:
							y_timestamps.append(base_time[event_announc[0]-1])
							#print("event_announc[0]: "+str(event_announc[0]))
							del event_announc[0]
				else:
					#print()
					y_timestamps.append(base_time[index])
					del event_announc[0]
					#print("event_announc:")
					#print(event_announc)
					#index +=1
					new_index = index
			else:
				'''
				if current_index_val != values_y[index][0]:
					current_index_count = 1
					current_index_val = values_y[index][0]'''
					#y_timestamps.append(values_y[index][1])
				if current_index_val == values_y[index][0]:
					current_index_count += 1
					#y_timestamps.append(start_time[index])

	#print("y_timestamps:")
	#print(y_timestamps)

	if len(y_timestamps) < 6:
		print("Less than 6 events")
		break

	new_y_timestamps = []
	len_y_sequences = 3 # output length (Y len)
	current_sequence_index = 1
	#print("new_y_timestamps:")
	new_y_timestamps.append(y_timestamps[0])
	for y_index in range(1,len(y_timestamps)):
		#print("y_index:"+str(y_index))
		if current_sequence_index <= len_y_sequences:
			if y_timestamps[y_index].split(":")[0] == new_y_timestamps[len(new_y_timestamps)-1].split(":")[0] or int(y_timestamps[y_index].split(":")[0]) == int(new_y_timestamps[len(new_y_timestamps)-1].split(":")[0])+1:
				new_y_timestamps.append(y_timestamps[y_index])
				timestamp_y = y_timestamps[y_index].split(":")[0]
				#print(y_timestamps[y_index])
				print(int(timestamp_y))
				current_sequence_index+=1
			else:
				while current_sequence_index < len_y_sequences:
					repeated_sequence = 1
					new_y_timestamps.append(new_y_timestamps[len(new_y_timestamps)-1]) #append the last element of the lost to the same list
					current_sequence_index+=1	
				new_y_timestamps.append(y_timestamps[y_index])
				current_sequence_index = 1
		else:
			new_y_timestamps.append(y_timestamps[y_index])
			current_sequence_index+=1

	while current_sequence_index < len_y_sequences:
		new_y_timestamps.append(new_y_timestamps[len(new_y_timestamps)-1]) #append the last element of the lost to the same list
		current_sequence_index+=1

	#print("len new_y_timestamps:")
	#print(len(new_y_timestamps))

	#print("new_y_timestamps:")
	#print(new_y_timestamps)

	if len(y_timestamps) == 0:
		print("No announcements events for peer " + peers_list[peer_id])
		exit()

	print("*** Event 1 ***")
	event_num = 2
	cont = 1
	for index in range(0,len(new_y_timestamps)):
		print(new_y_timestamps[index])
		if cont >= len_y_sequences:
			print("*** Event "+str(event_num)+" ***")
			#print(new_y_timestamps[index])
			event_num+=1
			cont = 0
		cont+=1
			
	#print("len y_timestamps:")
	#print(len(y_timestamps))

	list_num_updates = []
	list_timestamps_boundary = []
	#print(len(values))
	print(peers_list[peer_id])

	times_ip_dict = defaultdict(int)
	list_timestamps = []

	for index in range(0,num_timestamps-1):
		#print("Diference between number of updates at times: " + str(values[index][0]) + " and " + str(values[index+1][0]))
		diff_num_updates = abs(values[index][1] - values[index+1][1])
		if diff_num_updates > 0:
			list_timestamps_boundary.append(values[index][0]) 
		#print(diff_num_updates)
		if values[index][1] > 0:
			list_num_updates.append(values[index][1])
			list_timestamps.append(values[index][0])
			times_ip_dict[values[index][0]] = values[index][1]
		#list_num_updates.append(diff_num_updates)

	training_list = []
	for num_event in range(0,num_events*num_days):
		start_index = num_event * num_timestamps
		print("start_index: "+str(start_index))
		print(" ---- Event " + str(num_events*num_days) + "----- ")
		print(values[start_index:start_index+num_timestamps,])
		training_list.append(values[start_index:start_index+num_timestamps])

	#print("len training_list:")
	#print(len(training_list))
	#print(training_list)

	list_diff = []
	event_num = 1
	#print " ---- Event 1 ----- "
	for timestamp_index in range(0,len(list_timestamps_boundary)-1):
		diff_timestamps = datetime.strptime(list_timestamps_boundary[timestamp_index+1], FMT) - datetime.strptime(list_timestamps_boundary[timestamp_index], FMT)
		if diff_timestamps.seconds > 6900:
			event_num = event_num + 1 
			#print(" ---- Event " + str(event_num) + " ----- ")
		list_diff.append(diff_timestamps.seconds)
		#print("Inter-arrival: " + str(diff_timestamps.seconds))

	print(peers_list[peer_id])

	list_num_updates.sort(reverse=True)
	list_timestamps.sort()
	#print("list_num_updates:")
	#print(list_num_updates)

	#for index_updts in range(0,len(list_num_updates)):

	sum_updates = sum(list_num_updates)
	print("Sum list_num_updates:")
	print(sum_updates)

	mean_value = mean(list_num_updates)
	print("Mean number of Updates:")
	print(mean_value)

	times_ip_dict = OrderedDict(sorted(times_ip_dict.items(), key=lambda x: parse(x[0])))

	print("Timestamps with num_updates > 0:")
	print(times_ip_dict)

	filtered_times_ip_dict = defaultdict(int)
	for neighbor_ip in times_ip_dict.keys():
		if times_ip_dict[neighbor_ip] >= mean_value:
			filtered_times_ip_dict[neighbor_ip] = times_ip_dict[neighbor_ip]

	filtered_times_ip_dict = OrderedDict(sorted(filtered_times_ip_dict.items(), key=lambda x: parse(x[0])))
	#print("Filtered_times_ip_dict:")
	#print(filtered_times_ip_dict)

	number_timestamps = len(times_ip_dict)
	#print("Number of Timestamps:")
	#print(number_timestamps)

	training_x = []
	last_index = 0
	for x in range(0,num_days):
		current_index = last_index
		last_index = current_index
		for i in [0,2,4,6,8,10]:
			#print("i:"+str(i+last_index))
			current_index = last_index + i
			#print("current_index:")
			training_features = []
			for training_list_len in range(0,len(training_list[i+last_index])):
				#print("training_list[i+last_index][training_list_len]:")
				#print(training_list[i+last_index][training_list_len])
				#print(training_list[i+last_index][training_list_len][0])
				if datetime.strptime(training_list[i+last_index][training_list_len][0], FMT) < datetime.strptime(start_time[i], FMT):
					#print("Next day")
					tdelta = datetime.strptime(training_list[i+last_index][training_list_len][0], FMT) - datetime.strptime(start_time[i], FMT)
					#tdelta = tdelta.split(",")
					#tdelta = tdelta[1]
					#tdelta = tdelta.split(" ")[1]
					#print(tdelta.seconds)
					#print(str(tdelta.seconds)+" - "+str(training_list[i+last_index][training_list_len][0]))
					training_features.append(tdelta.seconds)
					training_features.append(training_list[i+last_index][training_list_len][1])
					training_features.append(training_list[i+last_index][training_list_len][2])
					training_features.append(training_list[i+last_index][training_list_len][3])
					training_features.append(training_list[i+last_index][training_list_len][4])
					training_features.append(training_list[i+last_index][training_list_len][5])
					training_features.append(training_list[i+last_index][training_list_len][6])
					training_features.append(training_list[i+last_index][training_list_len][7])
					training_features.append(training_list[i+last_index][training_list_len][8])
					training_features.append(training_list[i+last_index][training_list_len][9])
					training_features.append(training_list[i+last_index][training_list_len][10])
					training_features.append(training_list[i+last_index][training_list_len][11])
					training_features.append(training_list[i+last_index][training_list_len][12])
					training_features.append(training_list[i+last_index][training_list_len][13])
					training_features.append(training_list[i+last_index][training_list_len][14])
					training_features.append(training_list[i+last_index][training_list_len][15])
				else:
					tdelta = datetime.strptime(training_list[i+last_index][training_list_len][0], FMT) - datetime.strptime(start_time[i], FMT)
					#print(str(tdelta.seconds)+" - "+str(training_list[i+last_index][training_list_len][0]))
					training_features.append(tdelta.seconds)
					training_features.append(training_list[i+last_index][training_list_len][1])
					training_features.append(training_list[i+last_index][training_list_len][2])
					training_features.append(training_list[i+last_index][training_list_len][3])
					training_features.append(training_list[i+last_index][training_list_len][4])
					training_features.append(training_list[i+last_index][training_list_len][5])
					training_features.append(training_list[i+last_index][training_list_len][6])
					training_features.append(training_list[i+last_index][training_list_len][7])
					training_features.append(training_list[i+last_index][training_list_len][8])
					training_features.append(training_list[i+last_index][training_list_len][9])
					training_features.append(training_list[i+last_index][training_list_len][10])
					training_features.append(training_list[i+last_index][training_list_len][11])
					training_features.append(training_list[i+last_index][training_list_len][12])
					training_features.append(training_list[i+last_index][training_list_len][13])
					training_features.append(training_list[i+last_index][training_list_len][14])
					training_features.append(training_list[i+last_index][training_list_len][15])
			training_x.append(training_features)
		last_index = current_index + 2
		#print("last_index:" + str(last_index))
		if last_index >= len(training_list):
			break

	#print("training_x:")
	#print(training_x[0])

	training_y = []
	#print("Y values:")
	#print("new_y_timestamps: "+str(len(new_y_timestamps)))
	#print(new_y_timestamps)
	last_index = 0
	#last_index2 = 0
	training_y_lists = []
	for x in range(0,num_days):
		current_index = last_index
		last_index = current_index
		for j in range(0,len(base_time)/2):
			#print("j*2: "+str(j*2))
			#print("j+last_index: "+str(j+last_index))
			training_y_instance_list = []

			for num_array in range(0,len_y_sequences):
				current_index = last_index + num_array  
				if datetime.strptime(new_y_timestamps[num_array+last_index], FMT) < datetime.strptime(base_time[j*2], FMT):
					#print("new_y_timestamps[j+last_index+num_array]: "+str(new_y_timestamps[num_array+last_index]))
					#print("start_time[j*2]): "+str(base_time[j*2]))
					tdelta = datetime.strptime(new_y_timestamps[num_array+last_index], FMT) - datetime.strptime(base_time[j*2], FMT)
					training_y.append(tdelta.seconds)
					training_y_instance_list.append(tdelta.seconds)
				else:
					#print("new_y_timestamps[j+last_index+num_array]: "+str(new_y_timestamps[num_array+last_index]))
					#print("start_time[j*2]): "+str(base_time[j*2]))
					tdelta = datetime.strptime(new_y_timestamps[num_array+last_index], FMT) - datetime.strptime(base_time[j*2], FMT)
					training_y.append(tdelta.seconds)
					training_y_instance_list.append(tdelta.seconds)
					#last_index2 = current_index2 + 1
			last_index = current_index + 1 
			training_y_lists.append(training_y_instance_list)

	#print("training_y_lists")
	#print(training_y_lists)

	# normalize values for Y
	#y = np_utils
	#valuesY = pad_sequences(training_y, maxlen=1, dtype='float32')
	values_y = np.array(training_y_lists).reshape(-1,1) # transform valuesY to array
	scalerY = MinMaxScaler(feature_range=(0, 1))
	scaledY = scalerY.fit_transform(values_y)

	#values_y = pad_sequences(values_y, maxlen=1, dtype='float32')
	len_values_y = int(len(values_y)/len_y_sequences)
	scaledY = np.reshape(scaledY, (len_values_y,len_y_sequences))
	#scaledY = np.reshape(scaledY, (len(values_y)/6,6))
	print(scaledY.shape)
	#scaledY = np.reshape(scaledY,(6,6))

	print(values_y)
	print(scaledY)

	print("scaledY.shape: "+str(scaledY.shape))

	scalerX = MinMaxScaler(feature_range=(0, 1))
	scaledX = scalerX.fit_transform(training_x)

	# convert list of lists to array and pad sequences if needed
	X = pad_sequences(training_x, maxlen=seq_length, dtype='float32')
	print(X.shape)

	# reshape X to be [samples, time steps, features]
	#scaledX = np.reshape(training_x, (scaledX.shape[0], seq_length, 2))
	X = np.reshape(scaledX, (X.shape[0], seq_length, num_features))
	print(X.shape)

	# create and fit the model
	model = Sequential()
	model.add(LSTM(16, input_shape=(X.shape[1], X.shape[2])))
	model.add(Dropout(0.2))
	model.add(Dense(6, activation='relu'))
	model.add(Dense(scaledY.shape[1], activation='relu'))
	#model.add(Dense(scaledY.shape[1], activation='relu'))
	model.compile(loss='mae', optimizer='adam')
	#model.compile(loss='binary_crossentropy', optimizer='adam')
	model.fit(X, scaledY, epochs=num_epochs, batch_size=len(training_x)/2, validation_data=(X, scaledY), verbose=2, shuffle=False)

	list_models.append(model)

	prediction = model.predict(X, verbose=0)
	inv_yhat = scalerY.inverse_transform(prediction)
	#inv_yhat = inv_yhat[:,0]
	print("inv_yhat:")
	print(inv_yhat)

	inv_y = scalerY.inverse_transform(scaledY)
	#inv_y = inv_y[:,0]

	print "\n"
	#print "|  Predicted        -------       Real       "
	pred_len = len(prediction)
	print("pred_len: "+str(pred_len))
	iterator = 0

	while iterator < pred_len:
		#print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator],inv_y[iterator]) )
		#print(inv_yhat[iterator].tolist(),inv_y[iterator].tolist())
		print("|  PREDICTED       -------       TARGET")
		for predict_item in range(0,len(inv_yhat[iterator].tolist())):
			print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator].tolist()[predict_item],inv_y[iterator].tolist()[predict_item]) )	
		#print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator],inv_y[iterator]) )
		iterator += 1


for peer_id_index in range(0,len(list_peers)):
	print "Saving model for peer "+str(list_peers[peer_id_index])
	# serialize model to JSON
	model_json = list_models[peer_id_index].to_json()
	model_file_name = "model-"+str(list_peers[peer_id_index])+str(".json")
	with open(model_file_name, "w") as json_file:
    		json_file.write(model_json)
	# serialize weights to HDF5
	model_weights_name = 'lstm5_model-'+str(list_peers[peer_id_index])+'.h5'
	list_models[peer_id_index].save_weights(model_weights_name)


#################################################################################################################


#day_list = ["01","03","04","05","06","07"]
#day_list = ["08","09","10","11"]
#day_list = ["01","03","04","05","06","07","08","09","10","11","12","13","02"]
day_list = ["01-09","03-09","04-09","05-09","06-09","07-09","09-09","02-10","04-10","07-10","09-10","10-10","11-10","13-10"]
#day_list = ["01-09","03-09","04-09","05-09","06-09","07-09"]

for day in day_list:
	print("\n\n############################################### TEST DATASET ################################################")
	prediction_list = []
	target_list = []
	for peer_id_index in range(0,len(list_peers)):
		peer_id = list_peers[peer_id_index]
		print("\nTEST PEER "+str(peer_id))
		print("TEST PEER "+str(peers_list[peer_id]))
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

		if len(y_timestamps) == 0:
			print("No announcements events for peer " + peers_list[peer_id])
			exit()

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

		#print(training_list[0][0])
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

		#print(test_X.shape)
		if len(list_models) == 0:
			print("list_models")
			break

		print("peer_id_index: "+str(peer_id_index))
		print("len list_models: "+str(len(list_models)))

		prediction = list_models[peer_id_index].predict(test_X, verbose=0)
		inv_yhat = scalerY.inverse_transform(prediction)
		prediction_list.append(inv_yhat)
		#inv_yhat = inv_yhat[:,0]

		#print("prediction:")
		#print(prediction)

		#print("inv_yhat:")
		#print(inv_yhat)

		inv_y = scalerY.inverse_transform(scaledY)
		target_list.append(inv_y)

		print("\n")
		#print "|  Predicted        -------       Real       "
		pred_len = len(prediction)
		#print("pred_len: "+str(pred_len))

		#print("len(inv_yhat[iterator].tolist()):")
		#print(len(inv_yhat[0].tolist()))

		#print("inv_yhat[iterator].tolist():")
		#print(inv_yhat[0].tolist())

		#print("inv_y[iterator].tolist():")
		#print(inv_y[0].tolist())

		print("Prediction for peer: "+str(peer_id))
		iterator = 0
		while iterator < pred_len:
			#print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator],inv_y[iterator]) )
			#print(inv_yhat[iterator].tolist(),inv_y[iterator].tolist())
			print("|  PREDICTED       -------       TARGET")
			for predict_item in range(0,len(inv_yhat[iterator].tolist())):
				print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator].tolist()[predict_item],inv_y[iterator].tolist()[predict_item]) )	
			#print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator],inv_y[iterator]) )
			iterator += 1
		rmse_val = rmse(np.array(prediction_list), np.array(target_list))
		print("RMSE: " + str(rmse_val))

	#print("Prediction list:")
	#print(prediction_list)

	for peer_index in range(0,len(prediction_list)):
		print("Peer ID: "+str(peer_index))
		print(prediction_list[peer_index])

	for num_event in range(0,num_events/2):
		ct_list = []
		print("\n")
		print("Convergence Time lists for event: "+str(num_event))
		for peer_index in range(0,len(prediction_list)):
			print("Peer ID: "+str(peer_index))
			print(prediction_list[peer_index][num_event])
			for ct in range(0,len(prediction_list[peer_index][num_event])):
				if int(prediction_list[peer_index][num_event][ct]) != 0:
					ct_list.append(int(prediction_list[peer_index][num_event][ct]))
		print("ct_list:")
		print(ct_list)
		if len(ct_list) > 0:
			max_timestamp =  max(ct_list)
			min_timestamp =  min(ct_list)
			convergence_time = max_timestamp - min_timestamp
			print("max_timestamp: "+str(max_timestamp))
			print("min_timestamp: "+str(min_timestamp))
			print("Predicted Convergence Time: "+str(convergence_time))
		else:
			print("Predicted Convergence Time: 0")

		t_list = []
		print("\n")
		print("Target Convergence Time lists for event: "+str(num_event))
		for peer_index in range(0,len(target_list)):
			print("Peer ID: "+str(peer_index))
			print(target_list[peer_index][num_event])
			for ct in range(0,len(target_list[peer_index][num_event])):
				if int(target_list[peer_index][num_event][ct]) != 0:
					t_list.append(int(target_list[peer_index][num_event][ct]))
		print("target_list:")
		print(t_list)
		if len(t_list) > 0:
			max_timestamp =  max(t_list)
			min_timestamp =  min(t_list)
			convergence_time = max_timestamp - min_timestamp
			print("Target max_timestamp: "+str(max_timestamp))
			print("Target min_timestamp: "+str(min_timestamp))
			print("Target Convergence Time: "+str(convergence_time))
		else:
			print("Target Convergence Time: 0")

