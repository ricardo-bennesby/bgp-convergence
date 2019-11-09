from datetime import datetime

from dateutil.parser import parse
from collections import OrderedDict

from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

def take_features_in_time(list_times, file_num, prev_month, prefix, convergence_times_list,ct_index,index_file):
	prev_day = '../beacon_31-07-2018-yesterday/rrc'
	total_num_prefixes = set()
	total_number_announcements_1_min = 0
	total_number_withdrawals_1_min = 0
	shorter_as_path_len = 1000
	longer_as_path_len = 0
	total_as_path_len = 0
	as_path_set = set()
	number_duplicate_paths = 0
	peering_ases = set()
	prepend_as_set = set()
	number_prepended_ases = 0
	total_number_bytes = 0
	shortest_as_path = []
	num_announc_pref = 0
	num_withd_pref = 0
	num_pref_eq_24 = 0
	num_pref_long_24 = 0
	num_pref_short_24 = 0

	convergence_time_threshold = 6
	if convergence_times_list[ct_index] < convergence_time_threshold:
		print("convergence_times_list[ct_index] < convergence_time_threshold") 
		return None, convergence_time_threshold	

	#index_file = 0 #no previous file match prefix search
	for time_x in list_times:
		if len(time_x) == 7:
			time_x = '0'+time_x
		print('time_x:')
		print(time_x)
		if prev_month == 0:
			num_files = 288
		else:
			#num_files = 12 #used to files from past month (07-31-2018)
			num_files = 288

		num_time_x_file = 0 #count the number of prefixes in the file. If the prefix is not in file num_time_x_file==0 and index<-0
		if index_file != 0:
			file_name = './rrc' + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.08/file-' + str(index_file)
			#print(file_name)
			if prev_month == 0:
				file_name = './rrc' + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.08/file-' + str(index_file)
			else:
				#file_name = prev_day + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.07/file-' + str(index_file)	
				file_name = prev_day + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.07/file-' + str(index_file)
			print(file_name)
			try:
				with open(file_name) as f:
					line_count = 1
					for line in f:
						if time_x in line:
							num_time_x_file = num_time_x_file + 1
							#index_file = i #index of file where prefix was found
							#print("%s in file %s" % (time_x,file_name))
							line_fields = line.split('|')
							prefix_len = str(line_fields[4]).split('/')
							if len(prefix_len) > 1:
								if int(prefix_len[1]) == 24:
									num_pref_eq_24 = num_pref_eq_24 + 1
								elif int(prefix_len[1]) > 24:
									num_pref_long_24 = num_pref_long_24 + 1
								else:
									num_pref_short_24 = num_pref_short_24 + 1
							if prefix in line:
								if line_fields[1] == 'A':
									#the prefix was already announced in a previous timestamp
									num_announc_pref = num_announc_pref + 1 
								else:
									#the prefix was already withdrawn in a previous timestamp
									num_withd_pref = num_withd_pref + 1 
							total_num_prefixes.add(line_fields[4])
							peering_ases.add(line_fields[3])
							if line_fields[1] == 'A':
								total_number_bytes = total_number_bytes + int(line_fields[7])	
								#print line_fields
								as_path_list = line_fields[5].split(' ')
								#print "Duplicate AS_PATHs:"
								if line_fields[5] in as_path_set:
									number_duplicate_paths = number_duplicate_paths + 1
									#print line_fields[5]
								as_path_set.add(line_fields[5])
								for as_ in as_path_list:
									if as_ in prepend_as_set:
										number_prepended_ases = number_prepended_ases + 1
									prepend_as_set.add(as_)
								
					
								#print "AS_PATH Len:" + str(len(as_path_list))
								#print as_path_list
								total_as_path_len = total_as_path_len + len(as_path_list)
								if(len(as_path_list)) < shorter_as_path_len:
									shorter_as_path_len = len(as_path_list) 
									shortest_as_path = as_path_list
								if(len(as_path_list)) > longer_as_path_len:
									longer_as_path_len = len(as_path_list)
								total_number_announcements_1_min = total_number_announcements_1_min + 1
							else:
								total_number_withdrawals_1_min = total_number_withdrawals_1_min + 1
								total_number_bytes = total_number_bytes + int(line_fields[5])
			except IOError:
    				x = 1 # do nothing
		if num_time_x_file == 0:
			index_file = 0
			print("index <-0")	
		
		if index_file == 0: 
			for i in range(1,num_files):
				if prev_month == 0:
					file_name = './rrc' + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.08/file-' + str(i)
					#print file_name
				else:
					#file_name = prev_day + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.07/file-' + str(i)
					file_name = prev_day + file_num + '/data.ris.ripe.net/rrc' + file_num + '/2018.07/file-' + str(i)
					#print file_name
	
				try:
					with open(file_name) as f:
						line_count = 1
						for line in f:
							if time_x in line:
								index_file = i #index of file where prefix was found
								print("%s in file %s" % (time_x,file_name))
								line_fields = line.split('|')
								prefix_len = str(line_fields[4]).split('/')
								if len(prefix_len) > 1:
									if int(prefix_len[1]) == 24:
										num_pref_eq_24 = num_pref_eq_24 + 1
									elif int(prefix_len[1]) > 24:
										num_pref_long_24 = num_pref_long_24 + 1
									else:
										num_pref_short_24 = num_pref_short_24 + 1
								if prefix in line:
									if line_fields[1] == 'A':
										#the prefix was already announced in a previous timestamp
										num_announc_pref = num_announc_pref + 1 
									else:
										#the prefix was already withdrawn in a previous timestamp
										num_withd_pref = num_withd_pref + 1 
								total_num_prefixes.add(line_fields[4])
								peering_ases.add(line_fields[3])
								if line_fields[1] == 'A':
									total_number_bytes = total_number_bytes + int(line_fields[7])	
									#print line_fields
									as_path_list = line_fields[5].split(' ')
									#print "Duplicate AS_PATHs:"
									if line_fields[5] in as_path_set:
										number_duplicate_paths = number_duplicate_paths + 1
										#print line_fields[5]
									as_path_set.add(line_fields[5])
									for as_ in as_path_list:
										if as_ in prepend_as_set:
											number_prepended_ases = number_prepended_ases + 1
										prepend_as_set.add(as_)
								
					
									#print "AS_PATH Len:" + str(len(as_path_list))
									#print as_path_list
									total_as_path_len = total_as_path_len + len(as_path_list)
									if(len(as_path_list)) < shorter_as_path_len:
										shorter_as_path_len = len(as_path_list) 
										shortest_as_path = as_path_list
									if(len(as_path_list)) > longer_as_path_len:
										longer_as_path_len = len(as_path_list)
									total_number_announcements_1_min = total_number_announcements_1_min + 1
								else:
									total_number_withdrawals_1_min = total_number_withdrawals_1_min + 1
									total_number_bytes = total_number_bytes + int(line_fields[5])
				except IOError:
    					x = 1 # do nothing
				if index_file > 0:
					print("index_file > 0!")
					break

	features = []

	features.append(str(total_number_announcements_1_min))
	features.append(str(total_number_withdrawals_1_min))
	features.append(str(len(total_num_prefixes)))
	features.append(str(longer_as_path_len))
	features.append(str(shorter_as_path_len))
	features.append(str(total_as_path_len/total_number_announcements_1_min))
	features.append(str(number_duplicate_paths))
	features.append(str(len(peering_ases)))
	features.append(str(total_number_bytes/(total_number_announcements_1_min+total_number_withdrawals_1_min))) 
	features.append(str(number_prepended_ases/total_number_announcements_1_min))
	features.append(str(len(prepend_as_set))) 
	features.append(str(num_announc_pref))
	features.append(str(num_withd_pref))
	features.append(str(num_pref_eq_24)) 
	features.append(str(num_pref_long_24))
	features.append(str(num_pref_short_24))
	features.append(str(convergence_times_list[ct_index]))

	return (features,index_file)
