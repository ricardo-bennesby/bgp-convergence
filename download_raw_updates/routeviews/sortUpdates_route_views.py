from datetime import datetime

from dateutil.parser import parse
from collections import OrderedDict

from collections import defaultdict

data_dict = defaultdict(list)

number_announcements = 0
number_withdrawals = 0
list_of_times = []

update_dict = {}

distinct_ases = set()
peer_ases = set()

list_files = ['bgpdata','chile','eqix','flix','isc','jinx','kixp','linx','napafrica','nwax','perth','route-views3','route-views4','route-views6','saopaulo','saopaulo2','sfmix','sg','soxrs','sydney','telxatl','wide']

for i in list_files:
	file_name = 'log_file_' + i
	print file_name
	
	with open(file_name) as f:
		line_count = 1
    		for line in f:
        		line_fields = line.split('|')
			if "184.164.226.0/24" in line:
				if len(line_fields) > 5:
					#print "Time:" + line_fields[0] + " - Type:" + line_fields[1] + " - AS_PATH:" + line_fields[5]	 
					as_path_list = line_fields[5].split(' ')
					
					for as_ in as_path_list:
						distinct_ases.add(as_)
					peer_ases.add(as_path_list[0])
						
					#print "AS_PATH Len:" + str(len(as_path_list))
					#else:
					#print "Time:" + line_fields[0] + " - Type:" + line_fields[1]
				if line_fields[1] == 'A':
					number_announcements = number_announcements + 1
					update_dict.update({line_fields[0]:line_fields[5]})
					data_dict[line_fields[0]].append(line_fields[5])
					#data_dict.update({line_fields[0]:line_fields[5]})
				elif line_fields[1] == 'W':
					number_withdrawals = number_withdrawals + 1
					update_dict.update({line_fields[0]:line_fields[1]})
					data_dict[line_fields[0]].append(line_fields[1])
				list_of_times.append(line_fields[0])
				
				#print line_fields
				#print "Time:" + line_fields[0] + " - Type:" + line_fields[1] + " - AS_PATH:" + line_fields[5]
		
				line_count = line_count + 1

#print "len(update_dict)" + str(len(update_dict))

list_of_times.sort(key=lambda date: datetime.strptime(date, "%H:%M:%S"))
#print list_of_times

#print "len(list_of_times)" + str(len(list_of_times))

#print "len(data_dict)" + str(len(data_dict))

#list_of_times.sort(key=lambda date: datetime.strptime(date, "%H:%M:%S"))
#print list_of_times
	
FMT = '%H:%M:%S'
tdelta = datetime.strptime(list_of_times[len(list_of_times)-1], FMT) - datetime.strptime(list_of_times[0], FMT)

minutes = tdelta.seconds/60

print "Elapsed Time: " + str(tdelta) + " -- " + str(tdelta.seconds) + " seconds -- " + str(minutes) + " minutes."


new_d = OrderedDict(sorted(data_dict.items(), key=lambda x: parse(x[0])))
#new_d = OrderedDict(sorted(update_dict.items(), key=lambda x: parse(x[0])))

#for announcement in new_d:
#	print announcement, new_d[announcement]

shorter_as_path_len = 1000
longer_as_path_len = 0
start_event_time = list_of_times[0]
past_event_time = list_of_times[0]
time_out = 5
number_of_events = 1 
print "\nUpdates in the same event:"
for i in new_d:
	tdelta = datetime.strptime(i, FMT) - datetime.strptime(past_event_time, FMT)
	tdelta_event = datetime.strptime(past_event_time, FMT) - datetime.strptime(start_event_time, FMT)
	minutes = tdelta_event.seconds/60
	if (tdelta.seconds/60) < time_out:
		for j in new_d[i]:
			if len(j) > longer_as_path_len:
				longer_as_path_len = len(j)
				longer_as_path = j
			if len(j) < shorter_as_path_len and j!= 'W':
				shorter_as_path_len = len(j)
				shorter_as_path = j
			print i, j
	else:
		start_event_time = i
		number_of_events = number_of_events + 1
		print "Convergence Time: " + str(tdelta_event.seconds) + " seconds or " + str(minutes) + "min" + str(tdelta_event.seconds-minutes) + "s"
		print "\nUpdates in the same event:"
		for j in new_d[i]:
			print i, j
	past_event_time = i
print "Convergence Time: " + str(tdelta_event.seconds) + " seconds or " + str(minutes) + " min" + str(tdelta_event.seconds-minutes) + "s"
print "Number of events: " + str(number_of_events)

print "\n-----------------------------------------"

print "Number of Announcements: " + str(number_announcements)
print "Number of Withdrawals: " + str(number_withdrawals)
print "Number of reached ASes: " + str(len(distinct_ases))
print "Number of peer ASes: " + str(len(peer_ases))
print "Longer AS_PATH: " + longer_as_path
longer_as_path = longer_as_path.split(' ')
print "Longer AS_PATH Length: " + str(len(longer_as_path))
print "Shorter AS_PATH: " + shorter_as_path
shorter_as_path = shorter_as_path.split(' ')
print "Shorter AS_PATH Length: " + str(len(shorter_as_path))

print "-----------------------------------------"

				
