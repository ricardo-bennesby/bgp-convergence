import glob
import subprocess
import shlex

month = "10"
day = "22"

#files_list = glob.glob("./updates.*")
files_list = ["./updates.2018"+month+day+".1205.gz","./updates.2018"+month+day+".0805.gz","./updates.2018"+month+day+".0755.gz","./updates.2018"+month+day+".0220.gz","./updates.2018"+month+day+".1215.gz","./updates.2018"+month+day+".1800.gz","./updates.2018"+month+day+".2000.gz","./updates.2018"+month+day+".0010.gz","./updates.2018"+month+day+".2010.gz","./updates.2018"+month+day+".1755.gz","./updates.2018"+month+day+".2015.gz","./updates.2018"+month+day+".0810.gz","./updates.2018"+month+day+".0545.gz","./updates.2018"+month+day+".2205.gz","./updates.2018"+month+day+".1345.gz","./updates.2018"+month+day+".0615.gz","./updates.2018"+month+day+".2215.gz","./updates.2018"+month+day+".1545.gz","./updates.2018"+month+day+".0610.gz","./updates.2018"+month+day+".2145.gz","./updates.2018"+month+day+".0955.gz","./updates.2018"+month+day+".0945.gz","./updates.2018"+month+day+".2200.gz","./updates.2018"+month+day+".1600.gz","./updates.2018"+month+day+".2220.gz","./updates.2018"+month+day+".0145.gz","./updates.2018"+month+day+".0150.gz","./updates.2018"+month+day+".0400.gz","./updates.2018"+month+day+".1155.gz","./updates.2018"+month+day+".2355.gz","./updates.2018"+month+day+".1805.gz","./updates.2018"+month+day+".2020.gz","./updates.2018"+month+day+".0000.gz","./updates.2018"+month+day+".1210.gz","./updates.2018"+month+day+".1750.gz","./updates.2018"+month+day+".1945.gz","./updates.2018"+month+day+".0950.gz","./updates.2018"+month+day+".0555.gz","./updates.2018"+month+day+".1605.gz","./updates.2018"+month+day+".0215.gz","./updates.2018"+month+day+".0020.gz","./updates.2018"+month+day+".0745.gz","./updates.2018"+month+day+".1955.gz","./updates.2018"+month+day+".0420.gz","./updates.2018"+month+day+".0600.gz","./updates.2018"+month+day+".0750.gz","./updates.2018"+month+day+".0815.gz","./updates.2018"+month+day+".1610.gz","./updates.2018"+month+day+".0820.gz","./updates.2018"+month+day+".1015.gz","./updates.2018"+month+day+".1550.gz","./updates.2018"+month+day+".2005.gz","./updates.2018"+month+day+".1420.gz","./updates.2018"+month+day+".1350.gz","./updates.2018"+month+day+".1020.gz","./updates.2018"+month+day+".1145.gz","./updates.2018"+month+day+".1355.gz","./updates.2018"+month+day+".0345.gz","./updates.2018"+month+day+".1810.gz","./updates.2018"+month+day+".0015.gz","./updates.2018"+month+day+".2155.gz","./updates.2018"+month+day+".0350.gz","./updates.2018"+month+day+".1200.gz","./updates.2018"+month+day+".0405.gz","./updates.2018"+month+day+".0800.gz","./updates.2018"+month+day+".0210.gz","./updates.2018"+month+day+".1000.gz","./updates.2018"+month+day+".1620.gz","./updates.2018"+month+day+".2345.gz","./updates.2018"+month+day+".1010.gz","./updates.2018"+month+day+".0155.gz","./updates.2018"+month+day+".0200.gz","./updates.2018"+month+day+".1410.gz","./updates.2018"+month+day+".0415.gz","./updates.2018"+month+day+".1950.gz","./updates.2018"+month+day+".2210.gz","./updates.2018"+month+day+".2350.gz","./updates.2018"+month+day+".1415.gz","./updates.2018"+month+day+".2150.gz","./updates.2018"+month+day+".1220.gz","./updates.2018"+month+day+".0005.gz","./updates.2018"+month+day+".0205.gz","./updates.2018"+month+day+".1005.gz","./updates.2018"+month+day+".1555.gz","./updates.2018"+month+day+".1815.gz","./updates.2018"+month+day+".1400.gz","./updates.2018"+month+day+".0605.gz","./updates.2018"+month+day+".1615.gz","./updates.2018"+month+day+".0550.gz","./updates.2018"+month+day+".0410.gz","./updates.2018"+month+day+".0355.gz","./updates.2018"+month+day+".1820.gz","./updates.2018"+month+day+".1405.gz","./updates.2018"+month+day+".1150.gz","./updates.2018"+month+day+".1745.gz","./updates.2018"+month+day+".0620.gz"]

line_num = 0
for file_name in files_list:
	print str(line_num) + ":" + file_name
	line_num = line_num + 1
	f = open("file-"+str(line_num), "w")
	subprocess.call(shlex.split('python mrt2bgpdump.py '+file_name), stdout=f)
	
#subprocess.call(shlex.split('python mrt2bgpdump.py /home/ricardo/ripe/rrc03/19-06-2018/updates.20180619.1820.gz > newdata-'+str(line_num)+'.txt'))

#f = open("blah.txt", "w")

#subprocess.call(shlex.split('python mrt2bgpdump.py /home/ricardo/ripe/rrc03/19-06-2018/updates.20180619.1820.gz'), stdout=f)

