import sys
from datetime import datetime

from dateutil.parser import parse
from collections import OrderedDict

number_announcements = 0
number_withdrawals = 0
list_of_times = []

update_dict = {}

for i in range(1,47):
	file_name = 'file-' + str(i)
	#print file_name + ':'
	
	with open(file_name) as f:
		line_count = 1
    		for line in f:
        		if sys.argv[1] in line:
				print line
             			#print str(line_count) + ':' + line
				
