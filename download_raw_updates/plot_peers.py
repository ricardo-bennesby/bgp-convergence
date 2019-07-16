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

# specify columns to plot
groups = [0,1]
date = "01-09-2018"
FMT = '%H:%M:%S'
start_time = ['23:55:00','01:55:00','03:55:00','05:55:00','07:55:00','09:55:00','11:55:00','13:55:00','15:55:00','17:55:00','19:55:00','21:55:00']

peers_list = ['45.61.0.85', '80.77.16.114', '98.159.46.1', '146.228.1.3', '165.254.255.2', '168.195.130.2', '176.12.110.8', '178.255.145.243', '185.193.84.191', '192.102.254.1', '193.0.0.56', '193.138.216.164', '193.150.22.1', '193.160.39.1', '195.47.235.100', '203.119.104.1', '203.123.48.6', '208.51.134.248', '212.25.27.44', '213.200.87.254'] 

y_timestamps = []

'''
for peer_id in range(0,len(peers_list)):
	dataset = read_csv('timestamps-'+peers_list[peer_id]+'.csv')
	values = dataset.values
	print(peers_list[peer_id])
	print(values[:,0])
	print(values[:,1])
	x = values[180:300, 0]
	y = np.array(values[180:300, 1])

	pyplot.figure(figsize=(15,10))
	x = range(120)
	pyplot.xticks(x,  values[180:300, 0])
	locs, labels = pyplot.xticks()
	pyplot.setp(labels, rotation=90, fontsize=7)
	pyplot.title("Updates received per second at peer "+peers_list[peer_id]+" ["+date+"]")
	pyplot.ylabel("Number of Updates")

	#ataset.plot(kind='bar',x='timestamp',y=' count')
	pyplot.plot(x,y)
	#pyplot.title(dataset.columns[0], y=0.5, loc='right')
	#pyplot.show()
	#fig.suptitle('test title', fontsize=20)
	#pyplot.xlabel('xlabel', fontsize=5)
	pyplot.grid()
	pyplot.savefig('peers-'+peers_list[peer_id]+'.png')
	pyplot.clf()
	pyplot.cla()
	pyplot.close()
'''

#for peer_id in range(0,len(peers_list)):
peer_id = 16
num_events = 12
dataset = read_csv('/home/ricardo/ripe/databases_updates/timestamps-'+peers_list[peer_id]+'.csv')
values = dataset.values
num_timestamps = (len(values))/num_events

dataset_y = read_csv('/home/ricardo/ripe/databases_updates/times_after-'+peers_list[peer_id]+'.csv')
values_y = dataset_y.values

print("values_y:")
print(values_y)

event_announc = [1,3,5,7,9,11]
for index in range(0,len(values_y)):
	if int(values_y[index][0]) in event_announc:
		print(values_y[index][1]) 
		y_timestamps.append(values_y[index][1])
		del event_announc[0]

if len(y_timestamps) == 0:
	print("No announcements events for peer " + peers_list[peer_id])
	exit()

list_num_updates = []
list_timestamps_boundary = []
print(len(values))
print(peers_list[peer_id])

times_ip_dict = defaultdict(int)
list_timestamps = []


for index in range(0,num_timestamps-1):
	print("Diference between number of updates at times: " + str(values[index][0]) + " and " + str(values[index+1][0]))
	diff_num_updates = abs(values[index][1] - values[index+1][1])
	if diff_num_updates > 0:
		list_timestamps_boundary.append(values[index][0]) 
	print(diff_num_updates)
	if values[index][1] > 0:
		list_num_updates.append(values[index][1])
		list_timestamps.append(values[index][0])
		times_ip_dict[values[index][0]] = values[index][1]
	#list_num_updates.append(diff_num_updates)

training_list = []
for num_event in range(0,num_events):
	start_index = num_event * num_timestamps
	print(" ---- Event ----- ")
	#print(values[start_index:start_index+num_timestamps,])
	training_list.append(values[start_index:start_index+num_timestamps,])

print training_list[0]

list_diff = []
event_num = 1
print " ---- Event 1 ----- "
for timestamp_index in range(0,len(list_timestamps_boundary)-1):
	diff_timestamps = datetime.strptime(list_timestamps_boundary[timestamp_index+1], FMT) - datetime.strptime(list_timestamps_boundary[timestamp_index], FMT)
	if diff_timestamps.seconds > 6900:
		event_num = event_num + 1 
		#print(" ---- Event " + str(event_num) + " ----- ")
	list_diff.append(diff_timestamps.seconds)
	#print("Inter-arrival: " + str(diff_timestamps.seconds))

print("list_diff:")
print(list_diff)
print('##################')
print(set(list_diff))
print(Counter(list_diff))
df_list_diff = pd.DataFrame(pd.Series(Counter(list_diff).values()))
print df_list_diff	

#print("list_timestamps_boundary:")
#print(list_timestamps_boundary)

'''
print("list_num_updates:")
print(list_num_updates)

sum_updates = sum(list_num_updates)
print("Sum list_num_updates:")
print(sum_updates)
'''

print(peers_list[peer_id])

list_num_updates.sort(reverse=True)
list_timestamps.sort()
print("list_num_updates:")
print(list_num_updates)

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
print("Filtered_times_ip_dict:")
print(filtered_times_ip_dict)

number_timestamps = len(times_ip_dict)
print("Number of Timestamps:")
print(number_timestamps)

'''
for index in range(0,len(values)):
	diff_from_median = int(median_value) - int(values[index][1])
	print("time: "+values[index][0]+" - difference from median: "+str(abs(diff_from_median)))'''

'''
time_instance = times_ip_dict.keys()[1]
print("time_instance: "+time_instance)
print("Time differences:")
if datetime.strptime(time_instance, FMT) > datetime.strptime(start_time, FMT):
	print("Next day")
	tdelta = datetime.strptime(start_time, FMT) - datetime.strptime(time_instance, FMT)
	#tdelta = tdelta.split(",")
	#tdelta = tdelta[1]
	#tdelta = tdelta.split(" ")[1]
	print(tdelta.seconds)
else:
	tdelta = str(datetime.strptime(start_time, FMT) - datetime.strptime(time_instance, FMT))
	print(tdelta.seconds)'''
#print(time_instance - start_time)

print(training_list[0][0])
print("training_list:")
training_x = []
for i in [0,2,4,6,8,10]:
	print("i:"+str(i))
	training_features = []
	for training_list_len in range(0,len(training_list[i])):
		#print(training_list[0][training_list_len][0])
		if datetime.strptime(training_list[i][training_list_len][0], FMT) < datetime.strptime(start_time[i], FMT):
			#print("Next day")
			tdelta = datetime.strptime(training_list[i][training_list_len][0], FMT) - datetime.strptime(start_time[i], FMT)
			#tdelta = tdelta.split(",")
			#tdelta = tdelta[1]
			#tdelta = tdelta.split(" ")[1]
			#print(tdelta.seconds)
			print(str(tdelta.seconds)+" - "+str(training_list[i][training_list_len][1]))
			training_features.append(tdelta.seconds)
			training_features.append(training_list[i][training_list_len][1])
		else:
			tdelta = datetime.strptime(training_list[i][training_list_len][0], FMT) - datetime.strptime(start_time[i], FMT)
			print(str(tdelta.seconds)+" - "+str(training_list[i][training_list_len][1]))
			training_features.append(tdelta.seconds)
			training_features.append(training_list[i][training_list_len][1])
	training_x.append(training_features)

#y_timestamps = ['00:00:22','04:00:24','08:00:25','12:00:29','16:00:02','20:00:04']
training_y = []
#print("Y values:")
for j in range(0,len(y_timestamps)):
	if datetime.strptime(y_timestamps[j], FMT) < datetime.strptime(start_time[j*2], FMT):
		tdelta = datetime.strptime(y_timestamps[j], FMT) - datetime.strptime(start_time[j*2], FMT)
		training_y.append(tdelta.seconds)
	else:
		tdelta = datetime.strptime(y_timestamps[j], FMT) - datetime.strptime(start_time[j*2], FMT)
		training_y.append(tdelta.seconds)

#training_y = [22,24,25,29,2,4]

print((training_x))
print(training_y)

# normalize values for Y
#y = np_utils
#valuesY = pad_sequences(training_y, maxlen=1, dtype='float32')
values_y = np.array(training_y).reshape(-1,1) # transform valuesY to array
scalerY = MinMaxScaler(feature_range=(0, 1))
scaledY = scalerY.fit_transform(values_y)

print(values_y)
print(scaledY)

'''
# create and fit the model
model = Sequential()
model.add(LSTM(16, input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(y.shape[1], activation='relu'))
model.compile(loss='rmse', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=2000, batch_size=len(dataX), verbose=2, shuffle=False)'''

seq_length = 300

scalerX = MinMaxScaler(feature_range=(0, 1))
scaledX = scalerX.fit_transform(training_x)

# convert list of lists to array and pad sequences if needed
X = pad_sequences(training_x, maxlen=seq_length, dtype='float32')
print(X.shape)

# reshape X to be [samples, time steps, features]
#scaledX = np.reshape(training_x, (scaledX.shape[0], seq_length, 2))
X = np.reshape(scaledX, (X.shape[0], seq_length, 2))

print(X.shape)

# create and fit the model
model = Sequential()
model.add(LSTM(16, input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(scaledY.shape[1], activation='relu'))
model.compile(loss='mae', optimizer='adam')
#model.compile(loss='binary_crossentropy', optimizer='adam')
model.fit(X, scaledY, epochs=350, batch_size=len(training_x), verbose=2, shuffle=False)

# summarize performance of the model
scores = model.evaluate(X, scaledY, verbose=0)
print(scores)
print("Model Error: %.2f%%" % (scores*100))
#print(model.metrics_names)

# demonstrate some model predictions
#for pattern in X:
	#pattern = pad_sequences(pattern, maxlen=seq_length, dtype='float32')
	#print("pattern:")
	#print(pattern)
	#x = pad_sequences(training_x, maxlen=seq_length, dtype='float32')
	#x = np.reshape(pattern, (1, seq_length, 2))
	#print(x.shape)
	#scalerX = MinMaxScaler(feature_range=(0, 1))
	#scaledx = scalerX.fit_transform(x)
	
prediction = model.predict(X, verbose=0)
inv_yhat = scalerY.inverse_transform(prediction)
inv_yhat = inv_yhat[:,0]

inv_y = scalerY.inverse_transform(scaledY)
inv_y = inv_y[:,0]

print "\n"
print "|  Predicted        -------       Real       "
pred_len = len(prediction)
iterator = 0

while iterator < pred_len:
	#timestamp = float(int(inv_yhat[iterator]))
	#print("Timestamp:")
	#print(timestamp)
	#timestamp = datetime.fromtimestamp(float(inv_yhat[iterator]))
	#timestamp = datetime.fromtimestamp(timestamp)
	#print(start_time[iterator*2])
	#print("Timestamp:")
	#print(timestamp.strftime('%H:%M:%S'))
	#timestamp = datetime.strptime(start_time[iterator*2], FMT) - timestamp
	#print("Timestamp:")
	#print(timestamp)
	#print(timestamp.strftime('%H:%M:%S'))
	#timestamp_y = datetime.fromtimestamp(float(inv_y[iterator]))
	#print(timestamp_y.strftime('%H:%M:%S'))
	#tdelta_pred = datetime.strptime(str(int(inv_yhat[iterator])), FMT) + datetime.strptime(start_time[iterator*2], FMT)
	#tdelta_y = datetime.strptime(str(int(inv_y[iterator])), FMT) + datetime.strptime(start_time[iterator*2], FMT)
	#print(tdelta_pred)
	#print(tdelta_y)
	print("|   %.2f        -------        %.2f     " % (inv_yhat[iterator],inv_y[iterator]) )
	iterator += 1
#print(inv_yhat)

print(y_timestamps)

