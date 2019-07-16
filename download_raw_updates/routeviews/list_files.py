import glob
import subprocess
import shlex

month = "07"
day = "01"

#files_list = glob.glob("./updates.*")


files_list = ["./updates.2018"+month+day+".0430.bz2","./updates.2018"+month+day+".0230.bz2","./updates.2018"+month+day+".2145.bz2","./updates.2018"+month+day+".1830.bz2","./updates.2018"+month+day+".1400.bz2","./updates.2018"+month+day+".0215.bz2","./updates.2018"+month+day+".0815.bz2","./updates.2018"+month+day+".0945.bz2","./updates.2018"+month+day+".0615.bz2","./updates.2018"+month+day+".0145.bz2","./updates.2018"+month+day+".1630.bz2","./updates.2018"+month+day+".1430.bz2","./updates.2018"+month+day+".2015.bz2","./updates.2018"+month+day+".1230.bz2","./updates.2018"+month+day+".1600.bz2","./updates.2018"+month+day+".2230.bz2","./updates.2018"+month+day+".1800.bz2","./updates.2018"+month+day+".0830.bz2","./updates.2018"+month+day+".0630.bz2","./updates.2018"+month+day+".0000.bz2","./updates.2018"+month+day+".0600.bz2","./updates.2018"+month+day+".0415.bz2","./updates.2018"+month+day+".1545.bz2","./updates.2018"+month+day+".2030.bz2","./updates.2018"+month+day+".0745.bz2","./updates.2018"+month+day+".1345.bz2","./updates.2018"+month+day+".1415.bz2","./updates.2018"+month+day+".0545.bz2","./updates.2018"+month+day+".1200.bz2","./updates.2018"+month+day+".0200.bz2","./updates.2018"+month+day+".0400.bz2","./updates.2018"+month+day+".1030.bz2","./updates.2018"+month+day+".0015.bz2","./updates.2018"+month+day+".1745.bz2","./updates.2018"+month+day+".2000.bz2","./updates.2018"+month+day+".1000.bz2","./updates.2018"+month+day+".1015.bz2","./updates.2018"+month+day+".2215.bz2","./updates.2018"+month+day+".2345.bz2","./updates.2018"+month+day+".1145.bz2","./updates.2018"+month+day+".1215.bz2","./updates.2018"+month+day+".0800.bz2","./updates.2018"+month+day+".1945.bz2","./updates.2018"+month+day+".0030.bz2","./updates.2018"+month+day+".0345.bz2","./updates.2018"+month+day+".1615.bz2","./updates.2018"+month+day+".1815.bz2","./updates.2018"+month+day+".2200.bz2"]

line_num = 0
for file_name in files_list:
	print str(line_num) + ":" + file_name
	line_num = line_num + 1
	f = open("file-"+str(line_num), "w")
	subprocess.call(shlex.split('python mrt2bgpdump.py '+file_name), stdout=f)
	
#subprocess.call(shlex.split('python mrt2bgpdump.py /home/ricardo/ripe/rrc03/19-06-2018/updates.20180619.1820.gz > newdata-'+str(line_num)+'.txt'))

#f = open("blah.txt", "w")

#subprocess.call(shlex.split('python mrt2bgpdump.py /home/ricardo/ripe/rrc03/19-06-2018/updates.20180619.1820.gz'), stdout=f)

