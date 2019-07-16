from datetime import datetime

from dateutil.parser import parse
from collections import OrderedDict

from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

def take_features_in_time(list_times, file_num, prev_month, prefix, convergence_times_list,ct_index,index_file, peer_ip, peers_ip_counter_dict):
	#print "peer_ip:"
	#print peer_ip
	peer_time_list_announcements = []
	peer_time_list_withdrawals = []
	peer_time_list_duplicated = []
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

	#peers_dict_duplicated = defaultdict(int)
	peer_longest_as_path_dict = defaultdict(int)
	peer_shortest_as_path_dict = defaultdict(int)
	peer_avg_as_path_dict = defaultdict(int)
	prepended_ases_dict = defaultdict(int)
	tlong_dict = defaultdict(int)
	tshort_dict = defaultdict(int)
	avg_edit_distance_dict = defaultdict(int)
	maximum_edit_distance_dict = defaultdict(int)
	num_edited_paths_dict = defaultdict(int)
	num_announcements_peer_1_dict = defaultdict(int)
	num_announcements_peer_2_dict = defaultdict(int)
	num_announcements_peer_3_dict = defaultdict(int)

	prev_day = '../beacon_21-10-2018/rrc'
	total_num_prefixes = set()
	total_number_announcements_1_min = 0
	total_number_withdrawals_1_min = 0
	shorter_as_path_len = 1000
	longer_as_path_len = 0
	total_as_path_len = 0
	#as_path_set = set()
	number_duplicate_paths = 0
	peering_ases = set()
	#prepend_as_set = set()
	number_prepended_ases = 0
	total_number_bytes = 0
	shortest_as_path = []
	num_announc_pref = 0
	num_withd_pref = 0
	as_frequency_2_feature = 0
	neighbors_as_1 = set()
	neighbors_as_2 = set()
	distinct_ases = set()
	str_path_dict = defaultdict(list)
	str_path_dict_announcement = defaultdict(list)
	search_path_dict = defaultdict(list)
	search_path_dict_before = defaultdict(list)
	neighbor_ip_dict = defaultdict(list)
	frequent_neighbor_dict = defaultdict(lambda: defaultdict(int))
	announcing_as_ip = defaultdict(list)
	source_as_counter = 0
	FMT = '%H:%M:%S'
	list_timestamps_before = []

	convergence_time_threshold = 6
	if convergence_times_list[ct_index] < convergence_time_threshold:
		print "convergence_times_list[ct_index] < convergence_time_threshold" 
		return None, convergence_time_threshold	

	print("peers_ip_counter_dict:")
	print(peers_ip_counter_dict)

	#index_file = 0 #no previous file match prefix search
	for time_x in list_times:
		duplicated_announcements = 0
		announcement_set = set()
		prepended_as_set = set()
		unique_path_set = set()
		number_prepended_ases = 0
		tshort_events = 0
		tlong_events = 0
		as_path_set = set()
		peer_1 = 0
		peer_2 = 0
		peer_3 = 0
		edit_distance_list = []
		if len(time_x) == 7:
			time_x = '0'+time_x
		print 'time_x:'
		print time_x
		list_timestamps_before.append(time_x)
		if prev_month == 0:
			num_files = 288
		else:
			#num_files = 12 #used to files from past month (07-31-2018)
			num_files = 288

		num_time_x_file = 0 #count the number of prefixes in the file. If the prefix is not in file num_time_x_file==0 and index<-0
		if index_file != 0:
			file_name = './rrc' + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.10/file-' + str(index_file)
			if prev_month == 0:
				file_name = './rrc' + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.10/file-' + str(index_file)
			else:
				file_name = prev_day + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.10/file-' + str(index_file)
			print file_name
			try:
				with open(file_name) as f:
					line_count = 1
    					for line in f:
        					if time_x in line:
								num_time_x_file = num_time_x_file + 1
								line_fields = line.split('|')
								prefix_len = str(line_fields[4]).split('/')
								as_path_list = line_fields[5].split(' ')
								if str(line_fields[2]) == peer_ip:
									if str(line_fields[1]) == 'A':
										as_path_set.add(line_fields[5])
										peer_time_list_announcements.append(time_x) #for feature 1) Total Number of Announcements
										for path_index in announcement_set: 
											if line_fields[5] == path_index: #if line_fields[5] (AS_PATH) is already in announcement_set it is a duplicated path
												peer_time_list_duplicated.append(time_x)
												print("Duplicated path "+line_fields[5]+" from peer "+line_fields[2])
										announcement_set.add(line_fields[5]) #if line_fields[5] (AS_PATH) is not in duplicated it is added to the announcement_set
										as_path_list = line_fields[5].split(' ')
										print("as_path_list:")
										print(as_path_list)
										#remove_path = 0
										present_path = 0
										for as_path in unique_path_set:
											stored_as_path = as_path.split(' ')
											if stored_as_path[len(stored_as_path)-1] == as_path_list[len(as_path_list)-1]:
												unique_path_set.remove(as_path)
												unique_path_set.add(line_fields[5])
												present_path = 1
												print("****************************************************")
												print("Detected path to edit:")
												print("Replace \'"+as_path+"\' by \'"+line_fields[5]+"\'")
												if len(as_path_list) > len(stored_as_path):
													print("Difference length: "+str(len(as_path_list)-len(stored_as_path)))
													path_len_difference = len(as_path_list)-len(stored_as_path)
													num_path_mods = 0
													#In the following line we take the length of the shorter router to compare ASes, excluding the first and last dest AS_nums
													for as_index in range(1,len(stored_as_path)-1):
														if as_path_list[as_index] != stored_as_path[as_index]:
															num_path_mods += 1
													edit_distance = num_path_mods+path_len_difference
													print "EDIT DISTANCE: " + str(edit_distance)
													edit_distance_list.append(edit_distance)
													tlong_events += 1
												elif len(as_path_list) < len(stored_as_path):
													print("Difference length: "+str(len(stored_as_path)-len(as_path_list)))
													path_len_difference = len(stored_as_path)-len(as_path_list)
													num_path_mods = 0
													#In the following line we take the length of the shorter router to compare ASes, excluding the first and last dest AS_nums
													for as_index in range(1,len(as_path_list)-1):
														if as_path_list[as_index] != stored_as_path[as_index]:
															num_path_mods += 1
													edit_distance = num_path_mods+path_len_difference
													print "EDIT DISTANCE: " + str(edit_distance)
													edit_distance_list.append(edit_distance)
													tshort_events += 1
												else:
													print("Difference length: "+str(len(stored_as_path)-len(as_path_list)))
													path_len_difference = len(stored_as_path)-len(as_path_list)
													num_path_mods = 0
													#In the following line we take the length of the shorter router to compare ASes, excluding the first and last dest AS_nums
													for as_index in range(1,len(as_path_list)-1):
														if as_path_list[as_index] != stored_as_path[as_index]:
															num_path_mods += 1
													edit_distance = num_path_mods+path_len_difference
													print "EDIT DISTANCE: " + str(edit_distance)
													edit_distance_list.append(edit_distance)									
												break
										if len(unique_path_set) == 0 or present_path == 0:
											unique_path_set.add(line_fields[5])
										print("unique_path_set:")
										print(unique_path_set)	 
										for as_ in as_path_list:
											distinct_ases.add(as_)
											if as_ in prepended_as_set:
												number_prepended_ases = number_prepended_ases + 1
												print("Number of prepended: "+str(number_prepended_ases))
											prepended_as_set.add(as_)
										prepended_as_set = set()
										peer_ip_ases_len = len(peers_ip_counter_dict[peer_ip])
										print("peers_ip_counter_dict[peer_ip].keys():")
										print(peers_ip_counter_dict[peer_ip].keys())
										if len(as_path_list) > 1:
											if len(peers_ip_counter_dict[peer_ip].keys())>0:
												if int(as_path_list[1]) == peers_ip_counter_dict[peer_ip].keys()[0]:
													print("PEER AS #1: "+str(as_path_list[1]))
													peer_1 += 1
											if peer_ip_ases_len == 2:
												if int(as_path_list[1]) == peers_ip_counter_dict[peer_ip].keys()[1]:
													print("PEER AS #2: "+str(as_path_list[1]))
													peer_2 += 1 
											elif peer_ip_ases_len >= 3:
												if int(as_path_list[1]) == peers_ip_counter_dict[peer_ip].keys()[1]:
														print("PEER AS #2: "+str(as_path_list[1]))
														peer_2 += 1
												if int(as_path_list[1]) == peers_ip_counter_dict[peer_ip].keys()[2]:
													print("PEER AS #3: "+str(as_path_list[1]))
													peer_3 += 1 	
									else:
										peer_time_list_withdrawals.append(time_x)

			except IOError:
    				x = 1 # do nothing
		if num_time_x_file == 0:
			index_file = 0
			print "index <-0"	
		
		if index_file == 0: 
			for i in range(1,num_files):
				if prev_month == 0:
					file_name = './rrc' + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.10/file-' + str(i)
				else:
					file_name = prev_day + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.10/file-' + str(i)
				try:
					with open(file_name) as f:
						line_count = 1
    						for line in f:
        						if time_x in line:
									index_file = i #index of file where prefix was found
									print("%s in file %s" % (time_x,file_name))
									line_fields = line.split('|')
									as_path_list = line_fields[5].split(' ')
									if str(line_fields[2]) == peer_ip:
										if str(line_fields[1]) == 'A':
											as_path_set.add(line_fields[5])
											peer_time_list_announcements.append(time_x)
											for path_index in announcement_set: 
												if line_fields[5] == path_index: #if line_fields[5] (AS_PATH) is already in announcement_set it is a duplicated path
													peer_time_list_duplicated.append(time_x)
											announcement_set.add(line_fields[5]) #if line_fields[5] (AS_PATH) is not in duplicated it is added to the announcement_set
											as_path_list = line_fields[5].split(' ')
											print("as_path_list:")
											print(as_path_list)
											present_path = 0
											for as_path in unique_path_set:
												if as_path[len(as_path)-1] == as_path_list[len(as_path_list)-1]:
													unique_path_set.remove(as_path)
													unique_path_set.add(as_path_list)
													present_path = 1
													print("****************************************************")
													print("Detected path to edit:")
													print("Replace \'"+as_path+"\' by \'"+line_fields[5]+"\'")
													if len(as_path_list) > len(stored_as_path):
														print("Difference length: "+str(len(as_path_list)-len(stored_as_path)))
														path_len_difference = len(as_path_list)-len(stored_as_path)
														num_path_mods = 0
														#In the following line we take the length of the shorter router to compare ASes, excluding the first and last dest AS_nums
														for as_index in range(1,len(stored_as_path)-1):
															if as_path_list[as_index] != stored_as_path[as_index]:
																num_path_mods += 1
														edit_distance = num_path_mods+path_len_difference
														print "EDIT DISTANCE: " + str(edit_distance)
														edit_distance_list.append(edit_distance)
														tlong_events += 1
													elif len(as_path_list) < len(stored_as_path):
														print("Difference length: "+str(len(stored_as_path)-len(as_path_list)))
														path_len_difference = len(stored_as_path)-len(as_path_list)
														num_path_mods = 0
														#In the following line we take the length of the shorter router to compare ASes, excluding the first and last dest AS_nums
														for as_index in range(1,len(as_path_list)-1):
															if as_path_list[as_index] != stored_as_path[as_index]:
																num_path_mods += 1
														edit_distance = num_path_mods+path_len_difference
														print "EDIT DISTANCE: " + str(edit_distance)
														edit_distance_list.append(edit_distance)
														tshort_events += 1
													else:
														print("Difference length: "+str(len(stored_as_path)-len(as_path_list)))
														path_len_difference = len(stored_as_path)-len(as_path_list)
														num_path_mods = 0
														#In the following line we take the length of the shorter router to compare ASes, excluding the first and last dest AS_nums
														for as_index in range(1,len(as_path_list)-1):
															if as_path_list[as_index] != stored_as_path[as_index]:
																num_path_mods += 1
														edit_distance = num_path_mods+path_len_difference
														print "EDIT DISTANCE: " + str(edit_distance)
														edit_distance_list.append(edit_distance)
													break
											if len(unique_path_set) == 0 or present_path == 0:
												unique_path_set.add(line_fields[5])
											print("unique_path_set:")
											print(unique_path_set)	
											for as_ in as_path_list:
												distinct_ases.add(as_)
												if as_ in prepended_as_set:
													number_prepended_ases = number_prepended_ases + 1
													print("Number of prepended: "+str(number_prepended_ases))
												prepended_as_set.add(as_)
											prepended_as_set = set()
											peer_ip_ases_len = len(peers_ip_counter_dict[peer_ip])
											print("peers_ip_counter_dict[peer_ip].keys():")
											print(peers_ip_counter_dict[peer_ip].keys())
											if len(as_path_list) > 1:
												if len(peers_ip_counter_dict[peer_ip].keys())>0:
													if int(as_path_list[1]) == peers_ip_counter_dict[peer_ip].keys()[0]:
														print("PEER AS #1: "+str(as_path_list[1]))
														peer_1 += 1
												if peer_ip_ases_len == 2:
													if int(as_path_list[1]) == peers_ip_counter_dict[peer_ip].keys()[1]:
														print("PEER AS #2: "+str(as_path_list[1]))
														peer_2 += 1
												elif peer_ip_ases_len >= 3:
													if int(as_path_list[1]) == peers_ip_counter_dict[peer_ip].keys()[1]:
														print("PEER AS #2: "+str(as_path_list[1]))
														peer_2 += 1
													if int(as_path_list[1]) == peers_ip_counter_dict[peer_ip].keys()[2]:
														print("PEER AS #3: "+str(as_path_list[1]))
														peer_3 += 1 											
										else:
											peer_time_list_withdrawals.append(time_x)

				except IOError:
    					x = 1 # do nothing
				if index_file > 0:
					print "index_file > 0!"
					break
		#peers_dict_duplicated[time_x] = duplicated_announcements

		print("Edit distance list:")		
		print(edit_distance_list)
		num_edited_paths = 0
		if len(edit_distance_list) == 0:
			avg_edit_distance = float(0)
			maximum_edit_distance = 0
		else:
			avg_edit_distance = float(sum(edit_distance_list))/float(len(edit_distance_list))
			maximum_edit_distance = max(edit_distance_list)
			for edit_element in edit_distance_list:
				if edit_element != 0:
					num_edited_paths+=1
		print("Average Edit distance:")
		print(avg_edit_distance)
		print("maximum_edit_distance:")
		print(maximum_edit_distance)
		print("Number of edited paths:")
		print(num_edited_paths)

		print("PEER 1: "+str(peer_1))
		print("PEER 2: "+str(peer_2))
		print("PEER 3: "+str(peer_3))

		print("peer_time_list_duplicated:")
		print(peer_time_list_duplicated)
		print("peer_time_list_announcements:")
		print(peer_time_list_announcements)
		print("as_path_set:")
		print(as_path_set)
		print("Number of prepended ASes:")
		print(number_prepended_ases)
		longest_path_len = 0
		shortest_path_len = 100
		avg_path_len = 0
		total_path_len = 0
		for as_path_set_index in as_path_set:
			path_len = len(as_path_set_index.split(" "))
			if path_len > longest_path_len:
				longest_path_len = path_len
			if path_len < shortest_path_len:
				shortest_path_len = path_len
			total_path_len = total_path_len + path_len
			#print("path_len: "+str(path_len))
		if len(as_path_set) == 0:
			avg_path_len = 0
			shortest_path_len = 0
		else:	
			avg_path_len = total_path_len/len(as_path_set)
		print("Longest AS_PATH len: "+str(longest_path_len))
		print("Shortest AS_PATH len: "+str(shortest_path_len))
		print("Average AS_PATH len: "+str(avg_path_len))
		peer_longest_as_path_dict[time_x] = longest_path_len
		peer_shortest_as_path_dict[time_x] = shortest_path_len
		peer_avg_as_path_dict[time_x] = avg_path_len
		prepended_ases_dict[time_x] = number_prepended_ases
		tlong_dict[time_x] = tlong_events
		tshort_dict[time_x] = tshort_events
		avg_edit_distance_dict[time_x] = avg_edit_distance
		maximum_edit_distance_dict[time_x] = maximum_edit_distance
		num_edited_paths_dict[time_x] = num_edited_paths
		num_announcements_peer_1_dict[time_x] = peer_1
		num_announcements_peer_2_dict[time_x] = peer_2
		num_announcements_peer_3_dict[time_x] = peer_3
	peer_longest_as_path_list.append(peer_longest_as_path_dict)
	peer_shortest_as_path_list.append(peer_shortest_as_path_dict)
	peer_avg_as_path_list.append(peer_avg_as_path_dict)
	prepended_ases_list.append(prepended_ases_dict)
	tlong_list.append(tlong_dict)
	tshort_list.append(tshort_dict)
	avg_edit_distance_list.append(avg_edit_distance_dict)
	maximum_edit_distance_list.append(maximum_edit_distance_dict)
	num_edited_paths_list.append(num_edited_paths_dict)
	num_announcements_peer_1_list.append(num_announcements_peer_1_dict)
	num_announcements_peer_2_list.append(num_announcements_peer_2_dict)
	num_announcements_peer_3_list.append(num_announcements_peer_3_dict)

	#print("peer_longest_as_path_list:")
	#print(peer_longest_as_path_list)

	print("maximum_edit_distance_list:")
	print(maximum_edit_distance_list)

	print("tlong_list:")
	print(tlong_list)

	print("tshort_list:")
	print(tshort_list)

	features = []
	announcing_as_counter = len(announcing_as_ip)
	announcing_as_counter_ip = 0

	features.append(str(0))
	features.append(str(1))
	features.append(str(2))
	features.append(str(3))
	features.append(str(4))
	features.append(str(5))

	return (features, index_file, peer_time_list_announcements, peer_time_list_withdrawals, peer_time_list_duplicated, peer_longest_as_path_list, peer_shortest_as_path_list, peer_avg_as_path_list, prepended_ases_list, tlong_list, tshort_list, avg_edit_distance_list, maximum_edit_distance_list, num_edited_paths_list, num_announcements_peer_1_list, num_announcements_peer_2_list, num_announcements_peer_3_list, list_timestamps_before)
