from datetime import datetime
from dateutil.parser import parse
from collections import OrderedDict
from collections import defaultdict
from pandas import read_csv

from collect_features import *

import numpy as np
import matplotlib.pyplot as plt	

month = "06" # 27 days
month2 = "07" # 29 days
month3 = "08" # 27 days
month4 = "09" # 29 days
month5 = "10"
#month = "09"
#month2 = "07"
day_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","17","18","20","21","22","23","24","25","26","27","29","30"] #27
#day_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
day_list3 = ["01","02","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","26","27","28","29","30","31"] #27

day_list2 = ["01","02","03","04","05","06","07","08","09","10","11","12","13","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"] #29

#day_list4 = ["01","02","03","04","05","06","07","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
#day_list4 = ["01","02","03","04","05","06","07","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
#day_list5 = ["02","04","05","06","07"]

#day_list4 = ["01","02","03","04","05","06","07","09","10","11","12","13","15","16","17","18","20","21","22","23","24","25","26","27","28","29","30","31"]


#day_list = []
#day_list2 = []

#SELECTED:
#day_list3 = ["04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","26","27","28","29","30","31"]

#SELECTED:
day_list4 = ["01","03","04","05","06","07","09","10","11","13","15","16","18","20","22","23","25","26","27","28","29","30"] #22

#SELECTED:
#day_list5 = ["02","07","09","10","11","13","14","15","16","17","20","21","22","23","24","25","26","27","31"] #19
day_list5 = ["02","04","07","09","10","13","14","15","16","17","18","20","22","23","24","25","26","27","30","31"] #20


day_list5 = []

#day_list3 = ["19","20","21","22","26","27","28","29","30","31"]
#day_list2 = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
#day_list = ["01","02","03","04","05","06","07","08","09","10","11","12","14","15","17","18","20","21","22","23","24","25","26","27","29","30"]
#day_list2 = []
#day_list = []

timestamp_list = ["00:00:00","02:00:00","04:00:00","06:00:00","08:00:00","10:00:00","12:00:00","14:00:00","16:00:00","18:00:00","20:00:00","22:00:00"]

columnTitleRowAfter = "event_num,timestamp\n"
columnTitleRowTimestamp = "timestamp, num_announcements, num_withdrawals, duplicated_announc, longest_announc, shortest_announc, avg_announc, prepended_ases, tlongs, tshorts, avg_edit, maximum_edit, num_edits, announc_peer1, announc_peer2, announc_peer3\n"

def create_dataset_peers(times_after_db,timestamp_db):
	row_timestamp_db = ""
	#row_times_after_db = "1,23:55:00\n2,01:55:00\n3,03:55:00\n4,05:55:00\n5,07:55:00\n6,09:55:00\n7,11:55:00\n8,13:55:00\n9,15:55:00\n10,17:55:00\n11,19:55:00\n12,21:55:00\n"
	row_times_after_db = "1,00:00:00\n2,02:00:00\n3,04:00:00\n4,06:00:00\n5,08:00:00\n6,10:00:00\n7,12:00:00\n8,14:00:00\n9,16:00:00\n10,18:00:00\n11,20:00:00\n12,22:00:00\n"
	print("Created dataset for empty file")
	times_after_database = "times_after-"+peers_list[index]+".csv"
	times_after_db = open(times_after_database, "a")
	#times_after_db.write(columnTitleRowAfter)
	times_after_db.write(row_times_after_db)
	times_after_db.close()

	new_empty_timestampfile = "empty_timestamp_file.csv"
	
	timestamp_file = "timestamps-"+peers_list[index]+".csv"
	timestamp_db = open(timestamp_file, "a")
	#timestamp_db.write(columnTitleRowTimestamp)
	try:
		with open(new_empty_timestampfile) as f:
	   			for line in f:
	   				if "timestamp" not in line:
						timestamp_db.write(line)					
	except IOError:
			print("Error in writing to empty timestamp_file")	
	timestamp_db.close()
	#return row

'''empty_timestamp_array = []
empty_timestampfile = "empty_timestamp_file.csv"
try:
	with open(empty_timestampfile) as f:
	   		for line in f:
	   			timestamp_value = line.split(",")[0]
	   			#print(timestamp_value)
	   			empty_timestamp_array.append(timestamp_value)
	   			#if "timestamp" not in line:
				#	timestamp_db.write(line)					
except IOError:
	x = 1'''

peers_list = []
peers_list_file_csv = read_csv('/home/ricardo/ripe/databases_updates/peers_set.csv', header=None)
for peer_ip in peers_list_file_csv.values:
	#peers_list.add(announcement.tolist()[0])
	peers_list.append(peer_ip.tolist()[0])
print "peers_list after read_file:"
print peers_list

for index in range(0,len(peers_list)):
	#columnTitleRowAfter = "event_num,timestamp\n"
	#columnTitleRowTimestamp = "timestamp, num_announcements, num_withdrawals, duplicated_announc, longest_announc, shortest_announc, avg_announc, prepended_ases, tlongs, tshorts, avg_edit, maximum_edit, num_edits, announc_peer1, announc_peer2, announc_peer3\n"

	times_after_database = "times_after-"+peers_list[index]+".csv"
	times_after_db = open(times_after_database, "w")
	times_after_db.write(columnTitleRowAfter)
	times_after_db.close()

	timestamp_file = "timestamps-"+peers_list[index]+".csv"
	timestamp_db = open(timestamp_file, "w")
	timestamp_db.write(columnTitleRowTimestamp)
	timestamp_db.close()	


	for day in day_list:

		#open dataset from all collectors in a day
		database_train_times_aft = "./"+month+"-"+day+"/times_after-"+peers_list[index]+".csv"
		print database_train_times_aft

		database_train_timestamps = "./"+month+"-"+day+"/timestamps-"+peers_list[index]+".csv"
		print database_train_timestamps

		database_train_array = []
		timestamp_db = open(timestamp_file, "a")
		#is_empty_file = 0
		try:
			with open(database_train_timestamps) as f:
	    			for line in f:
	    				if "timestamp" not in line:
	    					#print(line)
	    					#database_train_array.append(line)
	    					timestamp_db.write(line)					
		except IOError:
				print("Error in Opening file timestamp_file")
				create_dataset_peers(times_after_db,timestamp_db)
				#is_empty_file = 1
				#x = 1 # do nothing
		'''if is_empty_file == 0:
			for empty_timestamp in empty_timestamp_array:
				for db_timestamp in database_train_array:
					if empty_timestamp == db_timestamp.split(",")[0]:
						database_train_array.append(db_timestamp)
					else:
						row = empty_timestamp+",0,0,0,0,0,0,0,0,0,0.0,0,0,0,0,0\n"'''

		times_after_db = open(times_after_database, "a")
		#list_indexes = [2,4,6,8,10,12]
		expected_index = 2
		has_index = 0
		try:
			with open(database_train_times_aft) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							#times_after_db.write(line)
							current_index = int(line.split(",")[0])
							if current_index <= expected_index:
								#print("expected_index: "+str(expected_index))
								#new_line = str(expected_index)+","+timestamp_list[expected_index-1]+"\n"
								times_after_db.write(line)
								#expected_index = expected_index + 1
								#expected_index = current_index	
								has_index = 1
							if current_index > expected_index:
								#times_after_db.write(line)
								#has_index = 1
								#expected_index = current_index + 1
								#print("current_index: "+str(current_index))
								#print("has_index: "+str(has_index))
								#print("expected_index: "+str(expected_index))
								if has_index == 0:
									#print("has_index == 0")
									line = str(expected_index)+","+timestamp_list[expected_index-1]+"\n"
									times_after_db.write(line)
									expected_index = expected_index + 2	
								else:
									times_after_db.write(line)
									#has_index = 1
									expected_index = current_index + 1
							'''else:
								if has_index == 0:
									print("expected_index: "+str(expected_index))
									line = str(expected_index)+","+timestamp_list[expected_index-1]
									times_after_db.write(line)
									expected_index = expected_index + 2
								else:
									has_index = 0'''
							#print(line)'''					
		except IOError:
				print("Error in Opening file times_after_database")
	    		#x = 1 # do nothing	    



	for day2 in day_list2:

		#open dataset from all collectors in a day
		database_train_times_aft = "./"+month2+"-"+day2+"/times_after-"+peers_list[index]+".csv"
		print database_train_times_aft

		database_train_timestamps = "./"+month2+"-"+day2+"/timestamps-"+peers_list[index]+".csv"
		print database_train_timestamps

		timestamp_db = open(timestamp_file, "a")
		try:
			with open(database_train_timestamps) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							timestamp_db.write(line)					
		except IOError:
				print("Error in Opening file timestamp_file")
				create_dataset_peers(times_after_db,timestamp_db)
	    		#x = 1 # do nothing

		times_after_db = open(times_after_database, "a")
		try:
			with open(database_train_times_aft) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							times_after_db.write(line)					
		except IOError:
				print("Error in Opening file times_after_database")
	    		#x = 1 # do nothing


	for day3 in day_list3:

		#open dataset from all collectors in a day
		database_train_times_aft = "./"+month3+"-"+day3+"/times_after-"+peers_list[index]+".csv"
		print database_train_times_aft

		database_train_timestamps = "./"+month3+"-"+day3+"/timestamps-"+peers_list[index]+".csv"
		print database_train_timestamps

		timestamp_db = open(timestamp_file, "a")
		try:
			with open(database_train_timestamps) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							timestamp_db.write(line)					
		except IOError:
				print("Error in Opening file timestamp_file")
				create_dataset_peers(times_after_db,timestamp_db)
	    		#x = 1 # do nothing

		times_after_db = open(times_after_database, "a")
		try:
			with open(database_train_times_aft) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							times_after_db.write(line)					
		except IOError:
				print("Error in Opening file times_after_database")
	    		#x = 1 # do nothing

	for day4 in day_list4:

		#open dataset from all collectors in a day
		database_train_times_aft = "./"+month4+"-"+day4+"/times_after-"+peers_list[index]+".csv"
		print database_train_times_aft

		database_train_timestamps = "./"+month4+"-"+day4+"/timestamps-"+peers_list[index]+".csv"
		print database_train_timestamps

		timestamp_db = open(timestamp_file, "a")
		try:
			with open(database_train_timestamps) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							timestamp_db.write(line)					
		except IOError:
				print("Error in Opening file timestamp_file")
				create_dataset_peers(times_after_db,timestamp_db)
	    		#x = 1 # do nothing

		times_after_db = open(times_after_database, "a")
		try:
			with open(database_train_times_aft) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							times_after_db.write(line)					
		except IOError:
				print("Error in Opening file times_after_database")

	for day5 in day_list5:

		#open dataset from all collectors in a day
		database_train_times_aft = "./"+month5+"-"+day5+"/times_after-"+peers_list[index]+".csv"
		print database_train_times_aft

		database_train_timestamps = "./"+month5+"-"+day5+"/timestamps-"+peers_list[index]+".csv"
		print database_train_timestamps

		timestamp_db = open(timestamp_file, "a")
		try:
			with open(database_train_timestamps) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							timestamp_db.write(line)					
		except IOError:
				print("Error in Opening file timestamp_file")
				create_dataset_peers(times_after_db,timestamp_db)
	    		#x = 1 # do nothing

		times_after_db = open(times_after_database, "a")
		try:
			with open(database_train_times_aft) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							times_after_db.write(line)					
		except IOError:
				print("Error in Opening file times_after_database")

#day_list = ["09-09","10-09","11-09","13-09","14-09","15-09","02-10"]
month = "09"
#day_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
#day_list = ["17","18","20","21","22","23","24","25","26","27","29","30"]
#day_list = ["09","10","11","13","14","15"]
#day_list = ["01","03","04","05","06"]
#day_list = ["01","02","03","04","05","06","07"]
day_list = []
#day_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]

month2 = "10"
#day_list2 = []
day_list2 = ["01","02","04","05","06","07","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

for index in range(0,len(peers_list)):
	columnTitleRowAfter = "event_num,timestamp\n"
	columnTitleRowTimestamp = "timestamp, num_announcements, num_withdrawals, duplicated_announc, longest_announc, shortest_announc, avg_announc, prepended_ases, tlongs, tshorts, avg_edit, maximum_edit, num_edits, announc_peer1, announc_peer2, announc_peer3\n"
	
	for day in day_list:

		times_after_database = "test-times_after-"+day+"-"+month+"-"+peers_list[index]+".csv"
		times_after_db = open(times_after_database, "w")
		times_after_db.write(columnTitleRowAfter)
		times_after_db.close()

		timestamp_file = "test-timestamps-"+day+"-"+month+"-"+peers_list[index]+".csv"
		timestamp_db = open(timestamp_file, "w")
		timestamp_db.write(columnTitleRowTimestamp)
		timestamp_db.close()

		#open dataset from all collectors in a day
		#database_train_times_aft = "./"+month+"-"+day+"/test-times_after-"+peers_list[index]+".csv"
		database_train_times_aft = "./"+month+"-"+day+"/times_after-"+peers_list[index]+".csv"
		print database_train_times_aft

		#database_train_timestamps = "./"+month+"-"+day+"/test-timestamps-"+peers_list[index]+".csv"
		database_train_timestamps = "./"+month+"-"+day+"/timestamps-"+peers_list[index]+".csv"
		print database_train_timestamps


		timestamp_db = open(timestamp_file, "a")
		try:
			with open(database_train_timestamps) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							timestamp_db.write(line)					
		except IOError:
	    		x = 1 # do nothing


		times_after_db = open(times_after_database, "a")
		try:
			with open(database_train_times_aft) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							times_after_db.write(line)					
		except IOError:
	    		x = 1 # do nothing


	for day2 in day_list2:

		times_after_database = "test-times_after-"+day2+"-"+month2+"-"+peers_list[index]+".csv"
		times_after_db = open(times_after_database, "w")
		times_after_db.write(columnTitleRowAfter)
		times_after_db.close()

		timestamp_file = "test-timestamps-"+day2+"-"+month2+"-"+peers_list[index]+".csv"
		timestamp_db = open(timestamp_file, "w")
		timestamp_db.write(columnTitleRowTimestamp)
		timestamp_db.close()

		#open dataset from all collectors in a day
		#database_train_times_aft = "./"+month2+"-"+day2+"/test-times_after-"+peers_list[index]+".csv"
		database_train_times_aft = "./"+month2+"-"+day2+"/times_after-"+peers_list[index]+".csv"
		print database_train_times_aft

		#database_train_timestamps = "./"+month2+"-"+day2+"/test-timestamps-"+peers_list[index]+".csv"
		database_train_timestamps = "./"+month2+"-"+day2+"/timestamps-"+peers_list[index]+".csv"
		print database_train_timestamps


		timestamp_db = open(timestamp_file, "a")
		try:
			with open(database_train_timestamps) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							timestamp_db.write(line)					
		except IOError:
	    		x = 1 # do nothing


		times_after_db = open(times_after_database, "a")
		try:
			with open(database_train_times_aft) as f:
	    			for line in f:
	    				if "timestamp" not in line:
							times_after_db.write(line)					
		except IOError:
	    		x = 1 # do nothing