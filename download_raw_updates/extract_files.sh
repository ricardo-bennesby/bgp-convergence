#!/bin/bash

#updates="updates.20180725*"
month="2018.10"

#for x in {00,01,03,04,05,06,07,10,11,12,13,14,15,16}; do
for x in {00,01,03,04,05,06,07,10,11,13,14,16}; do  
	cp "./list_files.py" "./rrc$x/data.ris.ripe.net/rrc$x/$month"
	cp "./mrt2bgpdump.py" "./rrc$x/data.ris.ripe.net/rrc$x/$month"
	#cp "./printLinePrefix.py" "./rrc$x/data.ris.ripe.net/rrc$x/$month" 
	cd ./rrc$x/data.ris.ripe.net/rrc$x/$month
	python list_files.py &
	cd -
done
