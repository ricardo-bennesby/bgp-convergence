from datetime import datetime
from dateutil.parser import parse
from collections import OrderedDict
from collections import defaultdict
from pandas import read_csv

from collect_features_peers import *

import numpy as np
import matplotlib.pyplot as plt	

update_type = "a"
test_dataset = 0

if update_type == "a":
	timeout = 6200
else:
	timeout = 120

prefix_collector_map = {"00": "84.205.64.0/24"}

def return_int(str_to_convert):
	if str_to_convert == "00":
		return 0
	elif str_to_convert == "01":
		return 1
	elif str_to_convert == "02":
		return 2
	elif str_to_convert == "03":
		return 3
	elif str_to_convert == "04":
		return 4
	elif str_to_convert == "05":
		return 5
	elif str_to_convert == "06":
		return 6
	elif str_to_convert == "07":
		return 7
	elif str_to_convert == "08":
		return 8
	elif str_to_convert == "09":
		return 9
	elif str_to_convert == "10":
		return 10
	elif str_to_convert == "11":
		return 11
	elif str_to_convert == "12":
		return 12
	elif str_to_convert == "13":
		return 13
	elif str_to_convert == "14":
		return 14
	elif str_to_convert == "15":
		return 15
	elif str_to_convert == "16":
		return 16
	elif str_to_convert == "17":
		return 17
	elif str_to_convert == "18":
		return 18
	elif str_to_convert == "19":
		return 19
	elif str_to_convert == "20":
		return 20
	elif str_to_convert == "21":
		return 21
	elif str_to_convert == "22":
		return 22

peers_list = ['45.61.0.85', '80.77.16.114', '98.159.46.1', '146.228.1.3', '165.254.255.2', '168.195.130.2', '176.12.110.8', '178.255.145.243', '185.193.84.191', '192.102.254.1', '193.0.0.56', '193.138.216.164', '193.150.22.1', '193.160.39.1', '195.47.235.100', '203.119.104.1', '203.123.48.6', '208.51.134.248', '212.25.27.44', '213.200.87.254','203.119.76.5','111.91.233.1','12.0.1.63','182.54.128.2','79.143.241.12','202.12.28.1'] 


prefix_set = set()
prefix_dict = defaultdict(list)
as_dict = defaultdict(int)
peers_dict_count = defaultdict(list)

peers_ip_counter_dict = defaultdict(lambda: defaultdict(int))

reset_peers_set = 0
write_new_peers_to_file = 0

peers_ip_before_announcement = []
peers_ip_before_withdrawal = []
peers_ip_before_duplicated = []
peers_ip_before_longest_pathlen = []
peers_ip_before_shortest_pathlen = []
peers_ip_before_avg_len = []
peers_ip_before_prepended = []
peers_ip_before_tlong = []
peers_ip_before_tshort = []
peers_ip_before_avg_edit_distance = []
peers_ip_before_maximum_edit_distance = []
peers_ip_before_num_edited = []
peers_ip_before_num_announcements_peer_1 = []
peers_ip_before_num_announcements_peer_2 = []
peers_ip_before_num_announcements_peer_3 = []
peers_ip_after = []

if test_dataset == 1:
	for peer_id in range(0,len(peers_list)):
		times_after_file = "test-times_after-"+peers_list[peer_id]+".csv"
		csv_after = open(times_after_file,"w")
		columnF = "event_num,timestamp\n"
		csv_after.write(columnF)
		csv_after.close()
else:
	for peer_id in range(0,len(peers_list)):
		times_after_file = "times_after-"+peers_list[peer_id]+".csv"
		csv_after = open(times_after_file,"w")
		columnF = "event_num,timestamp\n"
		csv_after.write(columnF)
		csv_after.close()

announcement_file = "announcement_dataset.csv"
csv = open(announcement_file,"w")
columnF = "edit_distance, repeated_paths, tshort, tlong, active_sessions, withdrawals, announcements, proportion, conv_time\n"
csv.write(columnF)
csv.close()

for file_rrc_name,prefix in prefix_collector_map.items():
	peers_set = set()
	peers_set_file = "/home/ricardo/ripe/databases_updates/peers_set.csv"
	if reset_peers_set:
		csv = open(peers_set_file,"w")
		csv.close()
	else: 
		peers_set_file_csv = read_csv('/home/ricardo/ripe/databases_updates/peers_set.csv' , header=None)
		for peer_ip in peers_set_file_csv.values:
			#peers_set.add(announcement.tolist()[0])
			peers_set.add(peer_ip.tolist()[0])
	print "peers_set after read_file:"
	print peers_set

	for peer_ip in peers_set:
		filename = '/home/ricardo/ripe/databases_updates/as_frequency-'+str(peer_ip)+'.csv'
		print("filename: "+filename)
		peers_ip_file = read_csv(filename, header=0)
		for peer in peers_ip_file.values:
			#print(peer.split("\n"))
			as_num = int(peer.tolist()[0])
			counter = int(peer.tolist()[1])
			#print("as_num: "+str(as_num))
			#print("counter: "+str(counter))
			peers_ip_counter_dict[peer_ip][as_num] = counter
		if len(peers_ip_counter_dict[peer_ip]) == 1:
			peers_ip_counter_dict[peer_ip][0] = 0
			peers_ip_counter_dict[peer_ip][0] = 0
		elif len(peers_ip_counter_dict[peer_ip]) == 2:
			peers_ip_counter_dict[peer_ip][0] = 0	
		peers_ip_counter_dict[peer_ip] = OrderedDict(sorted(peers_ip_counter_dict[peer_ip].items(), key=lambda x: x[1], reverse=True))

	#print("peers_ip_counter_dict:")
	#print(peers_ip_counter_dict) 

	#peers_list_file_csv = read_csv('/home/ricardo/ripe/databases_updates/peers_set.csv', header=0)

	#for peer in peers_set:
	#	peers_dict_count[peer].append("0")

	announcement_list = []
	dir_name = "./bases_beacon_rrc"+file_rrc_name+"/logs/"
	print(file_rrc_name,prefix)
	data_dict = defaultdict(list)
	announcing_as_set = set()
	list_neighbor_lists = []
	list_neighbor_ases = []
	list_announcing_times = []
	probable_paths = set()
	prev_month = 0

	number_announcements = 0
	number_withdrawals = 0
	list_of_times = []
	time_of_events = []

	#update_dict = {}
	update_dict = defaultdict(lambda: defaultdict(list))
	withdrawal_dict = defaultdict(lambda: defaultdict(list))

	distinct_ases = set()
	peer_ases = set()
	most_frequency_as_1 = []
	most_frequency_as_2 = []
	list_of_all_paths_day = set()
	neighbor_as_set = set()
	frequent_neighbor_as_set = set()
	frequent_neighbor_dict = defaultdict(lambda: defaultdict(list))
	frequent_neighbor_dict_count = defaultdict(lambda: defaultdict(int))
	frequent_as_dict = defaultdict(list)

	list_files = ['00','01','03','04','05','06','07','10','11','13','14','16','_bgpdata','_napafrica','_saopaulo','_sydney','_wide']
	list_files_db = ['00']

	file_num = file_rrc_name
	database_rrc = ""

	for i in list_files:
		file_name = 'log_file' + i
		print file_name
	
		with open(dir_name+file_name) as f:
			line_count = 1
    			for line in f:
        			line_fields = line.split('|')
				if prefix in line:
					if len(line_fields) > 5:
						as_path_list = line_fields[5].split(' ')
						if line_fields[5] in list_of_all_paths_day:
							list_of_all_paths_day -= {line_fields[5]}
							#print "Repeated path:"
							#print line_fields[5]
						else:
							list_of_all_paths_day.add(line_fields[5])
						#for as_ in as_path_list:
						#	distinct_ases.add(as_)
						peer_ases.add(as_path_list[0])
					if line_fields[1] == 'A':
						#print "Time:" + line_fields[0] + " - Type:" + line_fields[1] + " - Neighbor IP: " + line_fields[2] + " - AS_PATH:" + line_fields[5]
						#print line_fields[2] + " " + line_fields[5]
						if i=='00':
							prefix_set.add(line_fields[2])
							if line_fields[5] not in prefix_dict[line_fields[2]]:
								prefix_dict[line_fields[2]].append(line_fields[5])
						as_path_list = line_fields[5].split(" ")
						number_announcements = number_announcements + 1
						path_neighbor_ip = line_fields[5]+"-"+line_fields[2] 
						data_dict[line_fields[0]].append(path_neighbor_ip)
						update_dict[line_fields[5]][line_fields[2]].append(line_fields[0])
						frequent_neighbor_as_set.add(as_path_list[len(as_path_list)-2])
						if len(as_path_list) > 2:
							frequent_neighbor_dict[as_path_list[len(as_path_list)-2]][as_path_list[len(as_path_list)-3]].append(line_fields[0])
							frequent_neighbor_dict_count[as_path_list[len(as_path_list)-2]][as_path_list[len(as_path_list)-3]] = frequent_neighbor_dict_count[as_path_list[len(as_path_list)-2]][as_path_list[len(as_path_list)-3]] + 1
						else:
							frequent_neighbor_dict[as_path_list[len(as_path_list)-2]]['-'].append(line_fields[0])
							frequent_neighbor_dict_count[as_path_list[len(as_path_list)-2]]['-'] = frequent_neighbor_dict_count[as_path_list[len(as_path_list)-2]]['-'] + 1
						frequent_as_dict[as_path_list[len(as_path_list)-2]].append(line_fields[0])
					elif line_fields[1] == 'W':
						#print "Time:" + line_fields[0] + " - Type:" + line_fields[1] + " - Neighbor IP: " + line_fields[2]
						if i=='00':
							prefix_set.add(line_fields[2])
							#if line_fields[1] not in prefix_dict[line_fields[2]]:
								#prefix_dict[line_fields[2]].append(line_fields[1])
						number_withdrawals = number_withdrawals + 1
						path_neighbor_ip = line_fields[1]+"-"+line_fields[2]
						data_dict[line_fields[0]].append(path_neighbor_ip)
						update_dict['W'][line_fields[2]].append(line_fields[0])
					list_of_times.append(line_fields[0])
					line_count = line_count + 1
	list_of_times.sort(key=lambda date: datetime.strptime(date, "%H:%M:%S"))
	#print(list_of_times)
	
	FMT = '%H:%M:%S'
	tdelta = datetime.strptime(list_of_times[len(list_of_times)-1], FMT) - datetime.strptime(list_of_times[0], FMT)
	minutes = tdelta.seconds/60
	print "Elapsed Time: " + str(tdelta) + " -- " + str(tdelta.seconds) + " seconds -- " + str(minutes) + " minutes."
	new_d = OrderedDict(sorted(data_dict.items(), key=lambda x: parse(x[0])))

	shorter_as_path_len = 1000
	longer_as_path_len = 0
	time_out = timeout
	number_of_events = 1 
	convergence_times_list = []

	print "Set of prefixes:"
	print prefix_set
	print "Prefix_dict:"
	print prefix_dict

	announcement_times = 	["00:00:00","02:00:00","04:00:00","06:00:00","08:00:00","10:00:00","12:00:00","14:00:00","16:00:00","18:00:00","20:00:00","22:00:00"]
	#announcement_times = ["00:00:00","04:00:00","08:00:00","12:00:00","16:00:00","20:00:00"]
	withdrawals_times = ["02:00:00","06:00:00","10:00:00","14:00:00","18:00:00","22:00:00"]

	if update_type == "a":
		reference_beacon_times = announcement_times
		print "Announcement File"
	elif update_type == "w":
		reference_beacon_times = withdrawals_times
		print "Withdrawal File"

	time_of_events.append(reference_beacon_times[0])
	print "Reference Beacon Time of Events:"
	print reference_beacon_times

	beacon_reference_index = 0
	reference_beacon = reference_beacon_times[beacon_reference_index]
	past_event_time = reference_beacon
	start_event_time = reference_beacon
	number_updates_out_events = 0
	#number_updates_in_events = 0
	number_filtered_updates = 0

	print "\nUpdates in the same event:"
	past_in = reference_beacon
	unique_ases_after = set()
	num_repeated_paths = 0
	unique_paths_after = set()
	list_path_lens = []
	total_path_len = 0
	avg_path_len = 0
	std_deviation = 0
	as_frequency = {}
	list_all_announced_paths = []
	list_timestamps_one_event = []
	time_index = 0

	edit_paths = []
	total_edit_distance = 0
	total_num_repeated_paths = 0
	tshort_events = 0
	tlong_events = 0
	num_announcements_neighbors = 0
	num_withdrawals_neighbors = 0
	updates_proportion = 0
	active_sessions = set()
	last_timestamp = 0
	last_convergence_time = 0
	list_timestamps = []
	prefix_peers_set = set()
	announc_position = 1
	announcement_list_hours = [0,2,4,6,8,10,12,14,16,18,20,22]
	boundary = 0
	#first_announcement = 0
	num_event = 1

	for i in new_d:
		#print i
		set_past_event_time = 1
		current_hour = i.split(':')
		past_hour = past_in.split(':')
		current_hour = current_hour[0]
		past_hour1 = past_hour[0]
		#print current_hour
		current_hour_int = return_int(current_hour)
		#print("current_hour_int:")
		#print(current_hour_int)
		#print("announcement_list_hours[announc_position]:")
		#print(announcement_list_hours[announc_position])

		relative_time_seconds = datetime.strptime(i, FMT) - datetime.strptime(str(announcement_times[time_index]), FMT)
		tdelta = datetime.strptime(i, FMT) - datetime.strptime(past_event_time, FMT) #used for inter-arrival time between consecutive updates
		
		if current_hour_int == announcement_list_hours[announc_position]:
			if boundary != 1:
				relative_time_seconds = datetime.strptime(i, FMT) - datetime.strptime(str(announcement_times[time_index+1]), FMT)
			for j in new_d[i]:
				neighbor_ip = (j.split("-"))[1]
				if neighbor_ip in prefix_set:
					#print neighbor_ip
					#print i, relative_time_seconds.seconds
					peers_dict_count[neighbor_ip].append(i)
					print "neighbor_ip in prefix_set"
					prefix_peers_set.add(neighbor_ip)
					peers_set.add(neighbor_ip)	 
					print i, j, relative_time_seconds.seconds
					if test_dataset == 1:
						times_after_file = "test-times_after-"+neighbor_ip+".csv"
					else:
						times_after_file = "times_after-"+neighbor_ip+".csv"
					csv_after = open(times_after_file,"a")
					if boundary == 1:
						csv_after.write(str(num_event)+","+str(i)+"\n")
					else:
						csv_after.write(str(num_event+1)+","+str(i)+"\n")
					csv_after.close()

		if current_hour_int < announcement_list_hours[announc_position] or boundary == 1:
			#print "current_hour_int: " + str(current_hour_int)	
			#print("past_event_time: %s" % str(datetime.strptime(past_event_time, FMT)))
			#print("len delta: %s" % str(len(str(tdelta))))
		#if len(str(tdelta)) <= 8: # -1 day
			if number_filtered_updates != 0:
				print "Number of filtered updates: " + str(number_filtered_updates)
				print last_convergence_time
			number_filtered_updates = 0
			tdelta_event = datetime.strptime(past_event_time, FMT) - datetime.strptime(start_event_time, FMT) # for convergence time of event
			#print("*** tdelta: %s ***" % str(tdelta))
			minutes = tdelta_event.seconds/60
			#if (tdelta.seconds/60) < time_out:
			#print "tdelta.seconds: " + str(tdelta.seconds)
			if (tdelta.seconds) < time_out:
				list_timestamps_one_event.append(i)
				past_in = i
				for j in new_d[i]:
					relative_time_seconds = datetime.strptime(i, FMT) - datetime.strptime(str(announcement_times[time_index]), FMT)
					if len(j) > longer_as_path_len:
						longer_as_path_len = len(j)
						longer_as_path = j
					if len(j) < shorter_as_path_len and j!= 'W':
						shorter_as_path_len = len(j)
						shorter_as_path = j

					neighbor_ip = (j.split("-"))[1]
					neighbor_ip = (neighbor_ip.split(" "))[0]
					path = (j.split("-"))[0]
					active_sessions.add(neighbor_ip) 
					if neighbor_ip in prefix_set:
						peers_dict_count[neighbor_ip].append(i)
						print "neighbor_ip in prefix_set"
						prefix_peers_set.add(neighbor_ip)
						peers_set.add(neighbor_ip)	 
						print i, j, relative_time_seconds.seconds
						if test_dataset == 1:
							times_after_file = "test-times_after-"+neighbor_ip+".csv"
						else:
							times_after_file = "times_after-"+neighbor_ip+".csv"
						csv_after = open(times_after_file,"a")
						csv_after.write(str(num_event)+","+str(i)+"\n")
						csv_after.close()
						last_timestamp = relative_time_seconds.seconds
						list_timestamps.append(last_timestamp)
						if path != 'W':
							as_num = path.split(" ")[0]
							next_as_num = path.split(" ")[1]
							print "next_as_num:" + str(next_as_num)
							if as_num not in as_dict:
								as_dict[as_num] = 1
							else:
								as_dict[as_num] += 1
							num_announcements_neighbors += 1
							if len(edit_paths) == 0:
								edit_paths.append(path)
							else:
								path_presence = 0
								for path_i in range(0,len(edit_paths)):
									splitted_stored_ases = edit_paths[path_i].split(" ")
									splitted_current_ases = path.split(" ")
									if splitted_stored_ases[0] == splitted_current_ases[0]:
										print ".........................................."
										print "Detected path to edit:"
										print edit_paths[path_i] + " -> " + path
										if path == edit_paths[path_i]: 
											print "EDIT DISTANCE: 0"
											total_num_repeated_paths += 1
										else:
											if len(splitted_current_ases) > len(splitted_stored_ases):
												path_len_difference = len(splitted_current_ases)-len(splitted_stored_ases)
												num_path_mods = 0
												#In the following line we take the length of the shorter router to compare ASes, excluding the first and last dest AS_nums
												for as_index in range(1,len(splitted_stored_ases)-1):
													if splitted_current_ases[as_index] != splitted_stored_ases[as_index]:
														num_path_mods += 1
												edit_distance = num_path_mods+path_len_difference
												print "as_num: " + str(as_num)
												print "EDIT DISTANCE: " + str(edit_distance)
												total_edit_distance += edit_distance
												#print "Tlong event:"
												tlong_events += 1
												#print tlong_events	
											elif len(splitted_stored_ases) > len(splitted_current_ases):
												path_len_difference = len(splitted_stored_ases)-len(splitted_current_ases)
												num_path_mods = 0
												for as_index in range(1,len(splitted_current_ases)-1):
													if splitted_current_ases[as_index] != splitted_stored_ases[as_index]:
														num_path_mods += 1
												edit_distance = num_path_mods+path_len_difference
												print "EDIT DISTANCE: " + str(edit_distance)
												total_edit_distance += edit_distance
												#print "Tshort event:"
												tshort_events += 1
												#print tlong_events	
											else: #len(path) == len(edit_paths[path_i])
												path_len_difference = len(splitted_stored_ases)-len(splitted_current_ases)
												num_path_mods = 0
												for as_index in range(1,len(splitted_current_ases)-1):
													if splitted_current_ases[as_index] != splitted_stored_ases[as_index]:
														num_path_mods += 1
												edit_distance = num_path_mods+path_len_difference
												print "EDIT DISTANCE: " + str(edit_distance)
												total_edit_distance += edit_distance	
										#print ".........................................."
										previous_path = []
										for path_j in range(0,len(previous_path)):
											if path == previous_path[path_j]:
												"Flapping detected: " + path
										previous_path.append(edit_paths[path_i])
										edit_paths[path_i] = path
										path_presence = 1
								if path_presence == 0:
									edit_paths.append(path)
						else: #path == 'W':
							num_withdrawals_neighbors += 1
					as_path_len = len(j.split(" "))
					as_path_list = j.split(" ")
					distinct_ases.add(as_path_list[0])

					if str(as_path_list[len(as_path_list)-2])!= 'W':
						announcing_as_set.add(as_path_list[0])
					list_all_announced_paths.append(i+"-"+j)

					#print as_path_len
					list_path_lens.append(as_path_len)
					#number_updates_in_events = number_updates_in_events + 1
					if j in unique_paths_after:
						num_repeated_paths = num_repeated_paths + 1
					else:
						unique_paths_after.add(j)
					as_list = j.split(" ")

			if set_past_event_time == 1:
				past_event_time = i

		else:
			if announc_position == 11:
				boundary = 1
			else:
				announc_position += 1
			beacon_reference_index = beacon_reference_index + 1
			past_event_time = reference_beacon_times[beacon_reference_index]
			start_event_time = reference_beacon_times[beacon_reference_index]
			time_of_events.append(start_event_time)
			time_index = time_index + 1

			wtd_ann_proportion = 0
			if num_announcements_neighbors != 0:
				wtd_ann_proportion = int(float(num_withdrawals_neighbors)/float(num_announcements_neighbors)*100)
			else:
				last_timestamp = 0
			print "****************************************"
			print "FEATURES:"
			print "Total EDIT DISTANCE: " + str(total_edit_distance)
			print "Total Number of repeated_paths: " + str(total_num_repeated_paths)
			print "Tshort: " + str(tshort_events)
			print "Tlong: " + str(tlong_events)
			#print "Active Sessions: " + str(len(active_sessions))
			print "Active Sessions: " + str(len(prefix_peers_set))
			print "num_withdrawals_neighbors: " + str(num_withdrawals_neighbors)
			print "num_announcements_neighbors: " + str(num_announcements_neighbors)
			print "wtd_ann_proportion: " + str(wtd_ann_proportion)
			print "Number of filtered updates: " + str(number_filtered_updates)
			print "Relative Convergence Time: " + str(last_timestamp)
			print "Convergence Time: " + str(tdelta_event.seconds) + " seconds or " + str(minutes) + " min" + str(tdelta_event.seconds-minutes) + "s"
			convergence_times_list.append(tdelta_event.seconds)
			print "****************************************"
			print "prefix_peers_set:"
			print prefix_peers_set
			print "len prefix_peers_set:"
			print len(prefix_peers_set)
			print "peers_dict_count:"
			print peers_dict_count
			peers_ip_after.append(peers_dict_count)

			csv = open(announcement_file,"a")
			columnF = str(total_edit_distance) + "," + str(total_num_repeated_paths) + "," + str(tshort_events) + "," + str(tlong_events) + "," + str(len(prefix_peers_set)) + "," + str(num_withdrawals_neighbors) + "," + str(num_announcements_neighbors) + "," + str(wtd_ann_proportion) + "," + str(last_timestamp) + "\n"
			csv.write(columnF)
			csv.close()

			print "\nUpdates in the same event:"
			total_edit_distance = 0
			total_num_repeated_paths = 0
			tshort_events = 0
			tlong_events = 0
			num_withdrawals_neighbors = 0
			num_announcements_neighbors = 0
			number_filtered_updates = 0
			active_sessions = set()
			as_dict = defaultdict(int)
			list_timestamps = []
			prefix_peers_set = set()
			peers_dict_count = defaultdict(list)
			num_event += 1
	wtd_ann_proportion = 0
	if num_announcements_neighbors != 0:
		wtd_ann_proportion = int(float(num_withdrawals_neighbors)/float(num_announcements_neighbors)*100)
	print "****************************************"
	print "FEATURES:"
	print "Total EDIT DISTANCE: " + str(total_edit_distance)
	print "Total Number of repeated_paths: " + str(total_num_repeated_paths)
	print "Tshort: " + str(tshort_events)
	print "Tlong: " + str(tlong_events)
	#print "Active Sessions: " + str(len(active_sessions))
	print "Active Sessions: " + str(len(prefix_peers_set))
	print "num_withdrawals_neighbors: " + str(num_withdrawals_neighbors)
	print "num_announcements_neighbors: " + str(num_announcements_neighbors)
	print "wtd_ann_proportion: " + str(wtd_ann_proportion)
	print "Number of filtered updates: " + str(number_filtered_updates)
	print "Relative Convergence Time: " + str(last_timestamp)
	print "Convergence Time: " + str(tdelta_event.seconds) + " seconds or " + str(minutes) + " min" + str(tdelta_event.seconds-minutes) + "s"
	convergence_times_list.append(tdelta_event.seconds)
	print "****************************************"
	print "prefix_peers_set:"
	print prefix_peers_set
	print "len prefix_peers_set:"
	print len(prefix_peers_set)
	print "peers_dict_count:"
	print peers_dict_count
	peers_ip_after.append(peers_dict_count)

	csv = open(announcement_file,"a")
	columnF = str(total_edit_distance) + "," + str(total_num_repeated_paths) + "," + str(tshort_events) + "," + str(tlong_events) + "," + str(len(prefix_peers_set)) + "," + str(num_withdrawals_neighbors) + "," + str(num_announcements_neighbors) + "," + str(wtd_ann_proportion) + "," + str(last_timestamp) + "\n"
	csv.write(columnF)
	csv.close()

	if write_new_peers_to_file == 1:
		csv_peers = open(peers_set_file,"w")
		csv_peers.close()

		print peers_set
		print "len peers_set:"
		print len(peers_set)

		for peer in peers_set:
			csv_peers = open(peers_set_file, "a")
			row = str(peer) + "\n"
			csv_peers.write(row)
			csv_peers.close()

	FMT = '%H:%M:%S'
	time_range = []
	for num in range(1,31):
		if num>9:
			time_x = '00:00:'+str(num)
			time_range.append(time_x)
		else:
			time_x = '00:00:0'+str(num)
			time_range.append(time_x)

	print "List of times range:"
	print time_range
	print "time_range_len: " + str(len(time_range))

	number_timesteps = 9
	list_all_timestamps = []

	for j in range(0,len(time_of_events)):
		print "j:" + str(j)
		announcement_sample = defaultdict(int)
		announcement_dict = defaultdict(list)
		#announcement_list = []
		last_timestamp = ''
		list_times_before = []
		list_times_before2 = []

		total_list = []
		list_last_timestamps = []

		#print "TIME: " + time_of_events[j]
		for x in time_range:
			tdelta = datetime.strptime(time_of_events[j], FMT) - datetime.strptime(x, FMT)
			if len(str(tdelta)) > 8: # -1 day: take data from last day of previous month
				prev_month = 1
				tdelta = str(tdelta).split(',')
				tdelta = tdelta[1]
				tdelta = tdelta.split(' ')
				tdelta = tdelta[1]
			else:
				prev_month = 0
			list_times_before.append(str(tdelta))
			last_timestamp = str(tdelta) 
		total_list.append(list_times_before)
		list_last_timestamps.append(last_timestamp)
		
		for index in range(0,number_timesteps):	
			last_timestamp2 = ''
			list_times_before2 = []
			for x in time_range:
				tdelta2 = datetime.strptime(last_timestamp, FMT) - datetime.strptime(x, FMT)
				list_times_before2.append(str(tdelta2))
				last_timestamp2 = str(tdelta2)
				if len(last_timestamp) > 8: # -1 day: take data from last day of previous month
					last_timestamp = last_timestamp.split(',')
					last_timestamp = last_timestamp[1]
					last_timestamp = last_timestamp.split(' ')
					last_timestamp = last_timestamp[1]
			last_timestamp = last_timestamp2
			total_list.append(list_times_before2)

		ordered_total_list = []

		for index in range(0,len(total_list)-1):
			total_list[(len(total_list)-1)-index].sort(key=lambda date: datetime.strptime(date, "%H:%M:%S"))
			ordered_total_list.append(total_list[(len(total_list)-1)-index])

		total_list[0].sort(key=lambda date: datetime.strptime(date, "%H:%M:%S"))
		ordered_total_list.append(total_list[0])

		total_list = ordered_total_list

		print "total_list:"
		print total_list
		peer_ip_time_dict_announcement = defaultdict(list)
		peer_ip_time_dict_withdrawal = defaultdict(list)
		peer_ip_time_dict_duplicated = defaultdict(list)
		peer_ip_longest_dict = defaultdict(list)
		peer_ip_shortest_dict = defaultdict(list)
		peer_ip_avg_dict = defaultdict(list)
		peer_ip_prepended_dict = defaultdict(list)
		peer_ip_tlong_dict = defaultdict(list) 
		peer_ip_tshort_dict = defaultdict(list)  
		peer_ip_avg_edit_distance_dict = defaultdict(list) 
		peer_ip_maximum_edit_distance_dict = defaultdict(list)  
		peer_ip_num_edited_paths_dict = defaultdict(list)
		peer_ip_num_announcements_peer_1_dict = defaultdict(list)	
		peer_ip_num_announcements_peer_2_dict = defaultdict(list)
		peer_ip_num_announcements_peer_3_dict = defaultdict(list)		
		peer_time_list_announcements = []
		peer_time_list_withdrawals = []
		list_event_timestamps = []
		peer_longest_as_path_list = []
		peer_shortest_as_path_list = []
		peer_avg_as_path_list = []
		prepended_ases_list = []
		tlong_list = [] 
		tshort_list = []  
		avg_edit_distance_list = [] 
		maximum_edit_distance_list = []  
		num_edited_paths_list = []
		num_announcements_peer_1_list = []
		num_announcements_peer_2_list = []
		num_announcements_peer_3_list = []

		index_file = 0
		merge_lists = 1
		for peer_ip in peers_dict_count.keys():
			for index in range(0,len(total_list)):
				#print "time index:"
				#print index
				#print total_list[index]
				#list_of_features = None
				list_of_features, index_file, peer_time_list_announcements, peer_time_list_withdrawals, peer_time_list_duplicated, longest_as_path_list, shortest_as_path_list, avg_as_path_list, prepended_list, tlong_ases_list, tshort_ases_list, avg_edit_list, maximum_edit_list, num_edited_list, peer_1_list, peer_2_list, peer_3_list, list_timestamps_before = take_features_in_time(total_list[index], file_num, prev_month, prefix, convergence_times_list,j,index_file, peer_ip, peers_ip_counter_dict)
				#peers_before_times_dict_duplicated.update(peers_dict_duplicated)

				peer_longest_as_path_list = peer_longest_as_path_list + longest_as_path_list
				peer_shortest_as_path_list = peer_shortest_as_path_list + shortest_as_path_list
				peer_avg_as_path_list = peer_avg_as_path_list + avg_as_path_list
				prepended_ases_list = prepended_ases_list + prepended_list
				tlong_list = tlong_list + tlong_ases_list 
				tshort_list = tshort_list + tshort_ases_list  
				avg_edit_distance_list = avg_edit_distance_list + avg_edit_list 
				maximum_edit_distance_list = maximum_edit_distance_list + maximum_edit_list  
				num_edited_paths_list = num_edited_paths_list + num_edited_list 
				num_announcements_peer_1_list = num_announcements_peer_1_list + peer_1_list				
				num_announcements_peer_2_list = num_announcements_peer_2_list + peer_2_list
				num_announcements_peer_3_list = num_announcements_peer_3_list + peer_3_list

				if merge_lists == 1:
					list_event_timestamps = list_event_timestamps + list_timestamps_before
				for timestamp in peer_time_list_announcements:
					peer_ip_time_dict_announcement[peer_ip].append(timestamp)
				for timestamp in peer_time_list_withdrawals:
					peer_ip_time_dict_withdrawal[peer_ip].append(timestamp)
				for timestamp in peer_time_list_duplicated:
					peer_ip_time_dict_duplicated[peer_ip].append(timestamp)
				#print("peer_ip_time_dict_duplicated[peer_ip]:")
				#print(peer_ip_time_dict_duplicated[peer_ip])

				print("prepended_ases_list:")
				print(prepended_ases_list)
			
				if list_of_features != None:
					print "Range of values:" + str(total_list[index][0]) + "-" + str(total_list[index][len(total_list[index])-1])
					print "******* FEATURE VALUES: rrc" +  file_num +" *******"
					print "Announcing AS Counter: " + list_of_features[0]
					print "Announcing AS Counter IP: " + list_of_features[1]
					print "Number Path Dict before: " + list_of_features[2]
					print "Number AS-Pairs: " + list_of_features[3]
					print "Source AS Counter: " + list_of_features[4]
					print "Path presence: " + list_of_features[5]
					print "***************************"
				
			merge_lists = 0
			peer_ip_longest_dict[peer_ip] = peer_longest_as_path_list
			peer_ip_shortest_dict[peer_ip] = peer_shortest_as_path_list
			peer_ip_avg_dict[peer_ip] = peer_avg_as_path_list
			peer_ip_prepended_dict[peer_ip] = prepended_ases_list
			peer_ip_tlong_dict[peer_ip] = tlong_list 
			peer_ip_tshort_dict[peer_ip] = tshort_list  
			peer_ip_avg_edit_distance_dict[peer_ip] = avg_edit_distance_list 
			peer_ip_maximum_edit_distance_dict[peer_ip] = maximum_edit_distance_list  
			peer_ip_num_edited_paths_dict[peer_ip] = num_edited_paths_list
			peer_ip_num_announcements_peer_1_dict[peer_ip] = num_announcements_peer_1_list
			peer_ip_num_announcements_peer_2_dict[peer_ip] = num_announcements_peer_2_list			
			peer_ip_num_announcements_peer_3_dict[peer_ip] = num_announcements_peer_3_list

			peer_longest_as_path_list = []
			peer_shortest_as_path_list = []
			peer_avg_as_path_list = []
			prepended_ases_list = []
			tlong_list = []
			tshort_list = [] 
			avg_edit_distance_list = [] 
			maximum_edit_distance_list = []  
			num_edited_paths_list = []
			num_announcements_peer_1_list = []
			num_announcements_peer_2_list = []
			num_announcements_peer_3_list = []
			#print("peer_longest_as_path_list:")
			#print(peer_ip_longest_dict) 
			#print("peer_shortest_as_path_list:")
			#print(peer_ip_shortest_dict)
			#print("peer_avg_as_path_list:") 
			#print(peer_ip_avg_dict)
		list_all_timestamps.append(list_event_timestamps)

		print("peer_ip_time_dict_announcement:")
		print(peer_ip_time_dict_announcement)
		peers_ip_before_announcement.append(peer_ip_time_dict_announcement)
		peers_ip_before_withdrawal.append(peer_ip_time_dict_withdrawal)
		peers_ip_before_duplicated.append(peer_ip_time_dict_duplicated)
		peers_ip_before_longest_pathlen.append(peer_ip_longest_dict)
		peers_ip_before_shortest_pathlen.append(peer_ip_shortest_dict)
		peers_ip_before_avg_len.append(peer_ip_avg_dict)
		peers_ip_before_prepended.append(peer_ip_prepended_dict)
		peers_ip_before_tlong.append(peer_ip_tlong_dict) 
		peers_ip_before_tshort.append(peer_ip_tshort_dict) 
		peers_ip_before_avg_edit_distance.append(peer_ip_avg_edit_distance_dict)
		peers_ip_before_maximum_edit_distance.append(peer_ip_maximum_edit_distance_dict) 
		peers_ip_before_num_edited.append(peer_ip_num_edited_paths_dict)
		peers_ip_before_num_announcements_peer_1.append(peer_ip_num_announcements_peer_1_dict)
		peers_ip_before_num_announcements_peer_2.append(peer_ip_num_announcements_peer_2_dict)
		peers_ip_before_num_announcements_peer_3.append(peer_ip_num_announcements_peer_3_dict)
		#print("peers_ip_before_prepended:")
		#print(peers_ip_before_prepended)
		#print("list_event_timestamps:")
		#print(list_event_timestamps)

#print "peers_ip_before_announcement:"
#print peers_ip_before_announcement[0]

#print "peers_ip_after"
#print peers_ip_after[0]


for peer_id in peers_ip_before_announcement[0].keys():
	if test_dataset == 1:
		timestamp_file = "test-timestamps-"+peer_id+".csv"
	else:
		timestamp_file = "timestamps-"+peer_id+".csv"
	csv = open(timestamp_file,"w")
	columnF = "timestamp, num_announcements, num_withdrawals, duplicated_announc, longest_announc, shortest_announc, avg_announc, prepended_ases, tlongs, tshorts, avg_edit, maximum_edit, num_edits, announc_peer1, announc_peer2, announc_peer3\n"
	csv.write(columnF)
	csv.close()
		#times_after_file = "times_after-"+peer_id+".csv"
		#csv_after = open(times_after_file,"w")
		#columnF = "timestamp\n"
		#csv_after.write(columnF)
		#csv_after.close()

peers_before_times_dict_announcement = defaultdict(int)
peers_before_times_dict_withdrawal = defaultdict(int)
peers_before_times_dict_duplicated = defaultdict(int)
peers_before_times_dict_longest = defaultdict(int)
peers_before_times_dict_shortest = defaultdict(int)
peers_before_times_dict_avg = defaultdict(int)
peers_before_times_dict_prepended = defaultdict(int)
peers_before_times_dict_tlong = defaultdict(int)
peers_before_times_dict_tshort = defaultdict(int)
peers_before_times_dict_avg_edit = defaultdict(int)	
peers_before_times_dict_maximum_edit = defaultdict(int)
peers_before_times_dict_num_edit = defaultdict(int)
peers_before_times_dict_peer_1 = defaultdict(int)
peers_before_times_dict_peer_2 = defaultdict(int)
peers_before_times_dict_peer_3 = defaultdict(int)

for num_event in range(0,len(peers_ip_before_announcement)):
	print "--------------------------------"
	print "Event " + str(num_event) + ":"
	for peer_id in peers_ip_before_announcement[num_event].keys():
		list_peers_before_times_dict_announcement = []
		if test_dataset == 1:
			timestamp_file = "test-timestamps-"+peer_id+".csv"
		else:
			timestamp_file = "timestamps-"+peer_id+".csv"
		csv = open(timestamp_file,"a")
		print "peer neighbor IP:"
		print peer_id
		print "Timestamps before:"
		print peers_ip_before_announcement[num_event][peer_id]

		for timestamp in peers_ip_before_announcement[num_event][peer_id]:
			if timestamp not in peers_before_times_dict_announcement:
				peers_before_times_dict_announcement[timestamp] = 1
			else:
				peers_before_times_dict_announcement[timestamp] = 1 + peers_before_times_dict_announcement[timestamp]

		for timestamp in peers_ip_before_withdrawal[num_event][peer_id]:
			if timestamp not in peers_before_times_dict_withdrawal:
				peers_before_times_dict_withdrawal[timestamp] = 1
			else:
				peers_before_times_dict_withdrawal[timestamp] = 1 + peers_before_times_dict_withdrawal[timestamp]

		for timestamp in peers_ip_before_duplicated[num_event][peer_id]:
			if timestamp not in peers_before_times_dict_duplicated:
				peers_before_times_dict_duplicated[timestamp] = 1
			else:
				peers_before_times_dict_duplicated[timestamp] = 1 + peers_before_times_dict_duplicated[timestamp]

		#print("peers_ip_before_longest_pathlen[num_event][peer_id]:")
		#print(peers_ip_before_longest_pathlen[num_event][peer_id])

		print("peers_before_times_dict_duplicated:")
		print(peers_before_times_dict_duplicated)

		for list_index in range(0,len(peers_ip_before_longest_pathlen[num_event][peer_id])):
			#print("peers_ip_before_longest_pathlen[num_event][peer_id][list_index]:")
			#print(peers_ip_before_longest_pathlen[num_event][peer_id][list_index])
			for timestamp in peers_ip_before_longest_pathlen[num_event][peer_id][list_index].keys():
				peers_before_times_dict_longest[timestamp] = peers_ip_before_longest_pathlen[num_event][peer_id][list_index][timestamp] 

		for list_index in range(0,len(peers_ip_before_shortest_pathlen[num_event][peer_id])):
			for timestamp in peers_ip_before_shortest_pathlen[num_event][peer_id][list_index].keys():
				peers_before_times_dict_shortest[timestamp] = peers_ip_before_shortest_pathlen[num_event][peer_id][list_index][timestamp]

		for list_index in range(0,len(peers_ip_before_avg_len[num_event][peer_id])):
			for timestamp in peers_ip_before_avg_len[num_event][peer_id][list_index].keys():
				peers_before_times_dict_avg[timestamp] = peers_ip_before_avg_len[num_event][peer_id][list_index][timestamp]

		for list_index in range(0,len(peers_ip_before_prepended[num_event][peer_id])):
			for timestamp in peers_ip_before_prepended[num_event][peer_id][list_index].keys():
				peers_before_times_dict_prepended[timestamp] = peers_ip_before_prepended[num_event][peer_id][list_index][timestamp]

		for list_index in range(0,len(peers_ip_before_tlong[num_event][peer_id])):
			for timestamp in peers_ip_before_tlong[num_event][peer_id][list_index].keys():
				peers_before_times_dict_tlong[timestamp] = peers_ip_before_tlong[num_event][peer_id][list_index][timestamp]						

		for list_index in range(0,len(peers_ip_before_tshort[num_event][peer_id])):
			for timestamp in peers_ip_before_tshort[num_event][peer_id][list_index].keys():
				peers_before_times_dict_tshort[timestamp] = peers_ip_before_tshort[num_event][peer_id][list_index][timestamp]	

		for list_index in range(0,len(peers_ip_before_avg_edit_distance[num_event][peer_id])):
			for timestamp in peers_ip_before_avg_edit_distance[num_event][peer_id][list_index].keys():
				peers_before_times_dict_avg_edit[timestamp] = peers_ip_before_avg_edit_distance[num_event][peer_id][list_index][timestamp]

		for list_index in range(0,len(peers_ip_before_maximum_edit_distance[num_event][peer_id])):
			for timestamp in peers_ip_before_maximum_edit_distance[num_event][peer_id][list_index].keys():
				peers_before_times_dict_maximum_edit[timestamp] = peers_ip_before_maximum_edit_distance[num_event][peer_id][list_index][timestamp]
	
		for list_index in range(0,len(peers_ip_before_num_edited[num_event][peer_id])):
			for timestamp in peers_ip_before_num_edited[num_event][peer_id][list_index].keys():
				peers_before_times_dict_num_edit[timestamp] = peers_ip_before_num_edited[num_event][peer_id][list_index][timestamp]

		for list_index in range(0,len(peers_ip_before_num_announcements_peer_1[num_event][peer_id])):
			for timestamp in peers_ip_before_num_announcements_peer_1[num_event][peer_id][list_index].keys():
				peers_before_times_dict_peer_1[timestamp] = peers_ip_before_num_announcements_peer_1[num_event][peer_id][list_index][timestamp]

		for list_index in range(0,len(peers_ip_before_num_announcements_peer_2[num_event][peer_id])):
			for timestamp in peers_ip_before_num_announcements_peer_2[num_event][peer_id][list_index].keys():
				peers_before_times_dict_peer_2[timestamp] = peers_ip_before_num_announcements_peer_2[num_event][peer_id][list_index][timestamp]

		for list_index in range(0,len(peers_ip_before_num_announcements_peer_3[num_event][peer_id])):
			for timestamp in peers_ip_before_num_announcements_peer_3[num_event][peer_id][list_index].keys():
				peers_before_times_dict_peer_3[timestamp] = peers_ip_before_num_announcements_peer_3[num_event][peer_id][list_index][timestamp]

		'''for timestamp in peers_ip_before_longest_pathlen[num_event][peer_id].keys()
			peers_before_times_dict_longest[timestamp] = peers_ip_before_longest_pathlen[num_event][peer_id][timestamp]	

		for timestamp in peers_ip_before_shortest_pathlen[num_event][peer_id].keys()
			peers_before_times_dict_shortest[timestamp] = peers_ip_before_shortest_pathlen[num_event][peer_id][timestamp]

		for timestamp in peers_ip_before_avg_len[num_event][peer_id].keys()
			peers_before_times_dict_avg[timestamp] = peers_ip_before_avg_len[num_event][peer_id][timestamp]'''

		print "Timestamps after:"
		print peers_ip_after[num_event][peer_id]
		list_peers_before_times_dict_announcement.append(peers_before_times_dict_announcement)
		
		#print "peers_before_times_dict_announcement.keys():
		#print peers_before_times_dict_announcement.keys()

		print "peers_before_times_dict_longest:"
		print peers_before_times_dict_longest

		print "peers_before_times_dict_shortest:"
		print peers_before_times_dict_shortest

		row = ""
		for index in range(0,len(list_all_timestamps[num_event])):
		#for time_x in list_all_timestamps[num_event]:
			#if time_x in list_peers_before_times_dict_announcement.keys():

			#SAVE FEATURE 1) TIMESTAMP
			row = list_all_timestamps[num_event][index] + ","
	
			#SAVE FEATURE 2) TOTAL NUMBER OF ANNOUNCEMENTS
			if list_all_timestamps[num_event][index] in peers_before_times_dict_announcement.keys():
				#print time_x + ": " + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"
				#row = list_all_timestamps[num_event][index] + ",0\n"

			#SAVE FEATURE 3) TOTAL NUMBER OF WITHDRAWALS
			if list_all_timestamps[num_event][index] in peers_before_times_dict_withdrawal.keys():
				#print time_x + ": " + str(peers_before_times_dict_withdrawal[list_all_timestamps[num_event][index]])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_withdrawal[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_withdrawal[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 4) TOTAL NUMBER OF DUPLICATED ANNOUNCEMENTS
			if list_all_timestamps[num_event][index] in peers_before_times_dict_duplicated.keys():
				#print time_x + ": " + str(peers_before_times_dict_duplicated[list_all_timestamps[num_event][index]])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_duplicated[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_duplicated[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 5) LONGEST AS_PATH LENGTH
			if list_all_timestamps[num_event][index] in peers_before_times_dict_longest.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x]
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_longest[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_longest[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 6) SHORTEST AS_PATH LENGTH
			if list_all_timestamps[num_event][index] in peers_before_times_dict_shortest.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_shortest[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_shortest[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"			

			#SAVE FEATURE 7) AVERAGE AS_PATH LENGTH
			if list_all_timestamps[num_event][index] in peers_before_times_dict_avg.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_avg[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_avg[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0.0,"

			#SAVE FEATURE 8) NUMBER OF AS_PATHs WITH PREPENDED ASes
			if list_all_timestamps[num_event][index] in peers_before_times_dict_prepended.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_prepended[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_prepended[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 9) TLONG EVENTS
			if list_all_timestamps[num_event][index] in peers_before_times_dict_tlong.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_tlong[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_tlong[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 10) TSHORT EVENTS
			if list_all_timestamps[num_event][index] in peers_before_times_dict_tshort.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_tshort[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_tshort[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 11) AVERAGE OF EDIT DISTANCEs
			if list_all_timestamps[num_event][index] in peers_before_times_dict_avg_edit.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_avg_edit[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_avg_edit[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 12) MAXIMUM EDIT DISTANCE
			if list_all_timestamps[num_event][index] in peers_before_times_dict_maximum_edit.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_maximum_edit[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_maximum_edit[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 13) NUMBER OF EDIT DISTANCEs > 0
			if list_all_timestamps[num_event][index] in peers_before_times_dict_num_edit.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_num_edit[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_num_edit[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"	

			#SAVE FEATURE 14) NUMBER OF ANNOUNCEMENTS FROM PEER #1
			if list_all_timestamps[num_event][index] in peers_before_times_dict_peer_1.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_peer_1[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_peer_1[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"

			#SAVE FEATURE 15) NUMBER OF ANNOUNCEMENTS FROM PEER #2
			if list_all_timestamps[num_event][index] in peers_before_times_dict_peer_2.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_peer_2[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_peer_2[list_all_timestamps[num_event][index]]) + ","
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0,"															

			#SAVE FEATURE 16) NUMBER OF ANNOUNCEMENTS FROM PEER #3
			if list_all_timestamps[num_event][index] in peers_before_times_dict_peer_3.keys():
				#print time_x + ": " + str(list_peers_before_times_dict_announcement[time_x])
				print list_all_timestamps[num_event][index] + ": " + str(peers_before_times_dict_peer_3[list_all_timestamps[num_event][index]])
				#row = list_all_timestamps[num_event][index] + "," + str(peers_before_times_dict_announcement[list_all_timestamps[num_event][index]]) + "\n"
				row = row + str(peers_before_times_dict_peer_3[list_all_timestamps[num_event][index]]) + "\n"
			else:
				print list_all_timestamps[num_event][index] + ": 0"
				row = row + "0\n"

			csv.write(row)
		csv.close()
				
		peers_before_times_dict_announcement = defaultdict(int)
		peers_before_times_dict_withdrawal = defaultdict(int)
		peers_before_times_dict_duplicated = defaultdict(int)
		peers_before_times_dict_longest = defaultdict(int)
		peers_before_times_dict_shortest = defaultdict(int)
		peers_before_times_dict_avg = defaultdict(int)
		print list_peers_before_times_dict_announcement

print list_all_timestamps
print "len list_all_timestamps:"
print len(list_all_timestamps)

print "list_peers_before_times_dict_announcement:"
print list_peers_before_times_dict_announcement


