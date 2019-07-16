from pandas import read_csv
from pandas import DataFrame
import pandas as pd
import time

# fix random seed for reproducibility
#numpy.random.seed(7)

db_type = "lstm5"
update_type = 'a'
month = '09'
day = '01'
date = month+'-'+day
num_epochs=5000
batch=2
num_experiments = 1
error_scores = list()

announcement_times = ["23:5","-3:5","-7:5","-11:5","-15:5","-19:5"]
announc_index = 0

#------------------------------------------------------------------------------------

# load dataset
#dataset = read_csv('convergence_features-aX.csv', header=0, index_col=0)
#dataset = read_csv('convergence_features-rrc00-wX.csv', header=0, index_col=0)
#dataset = read_csv('convergence_features-rrc01-aX.csv', header=0, index_col=0)

#cols = list(read_csv('convergence_features_lstm5_train-a.csv', nrows =1))
#print(cols)

#dataset = read_csv('convergence_features_'+db_type+'_previous_train-'+update_type+'.csv')
#dataset = read_csv('convergence_features-rrc00-a-previous-t5.csv')
dataset = read_csv('convergence_features-rrc00-a-previous-t5.csv')
#dataset.drop(' num_announc_pref',axis=1,inplace=True)
#dataset.drop(' num_withd_pref',axis=1,inplace=True)

values = dataset.values
# ensure all data is float
#values = values.astype('float32')

database_file = "num_events-"+update_type+"-t5.csv" #where you want the file to be downloaded to 
csv = open(database_file, "w")
columnTitleRow = "time, num_events\n"
csv.write(columnTitleRow)
csv.close()

num_updates = 0
print "index_col:"
event_indexes = []

database_file = "num_events-"+update_type+"-t5.csv" #where you want the file to be downloaded to 
csv = open(database_file, "a")
row = str(announcement_times[0]) + "," + str(0) + "\n"
csv.write(row)

start_time = time.time()
elapsed_time = 0

print "len(announcement_times): " + str(len(announcement_times))
for i in range(0,len(dataset.values)):
	time_x = dataset.values[i]
	#print time[0]
	if announc_index + 1 >= len(announcement_times):
		print "Reached announcement_times list length"
		#announc_index = 0
		break
	if str(announcement_times[announc_index]) in str(time_x[0]):
		num_updates = num_updates + 1
		#print "Event " + str(announc_index+1) + ": " + str(num_updates) + " updates"
	else: 
		end_time = time.time()
		elapsed_time = (end_time - start_time) + elapsed_time
		print elapsed_time, "seconds"
		start_time = time.time()
		print time_x[0]
		row = str(announcement_times[announc_index+1]) + "," + str(num_updates) + "\n"
		csv.write(row)
		csv.close()
		csv = open(database_file, "a")
		event_indexes.append(num_updates)
		announc_index = announc_index + 1
		print "announc_index: " + str(announc_index)
		num_updates = num_updates + 1
		#num_updates = 0

print "event_indexes:"
print event_indexes
print "Total elapsed time: " + str(elapsed_time/60) + " minutes."

csv.close()
