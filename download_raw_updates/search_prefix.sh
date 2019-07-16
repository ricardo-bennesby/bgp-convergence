#!/bin/bash

#updates="updates.20110709*"
month="2018.10"
current_date="22_10_2018"


collector="00"
prefix="84.205.64.0/24"

mkdir bases_beacon_rrc$collector && cd bases_beacon_rrc$collector && pwd
mkdir logs 
cd .. 
pwd

for x in {00,01,03,04,05,06,07,10,11,13,14,16}; do  
	cp "./trackLinePrefix.py" "./rrc$x/data.ris.ripe.net/rrc$x/$month"
	cd ./rrc$x/data.ris.ripe.net/rrc$x/$month 
	python trackLinePrefix.py $prefix  > log_file$x
	cd -
	cp "./rrc$x/data.ris.ripe.net/rrc$x/$month/log_file$x" "./"
	cp "log_file$x" "./bases_beacon_rrc$collector/logs"
	rm "log_file$x"
done

for y in {log_file_bgpdata,log_file_linx,log_file_napafrica,log_file_saopaulo,log_file_sydney,log_file_wide}; do
	cp "../../route-views/beacon_logs_rv_$current_date/rrc$collector/$y" "./bases_beacon_rrc$collector/logs"
done



collector="01"
prefix="84.205.65.0/24"

mkdir bases_beacon_rrc$collector && cd bases_beacon_rrc$collector && pwd
mkdir logs 
cd .. 
pwd

for x in {00,01,03,04,05,06,07,10,11,13,14,16}; do  
	cp "./trackLinePrefix.py" "./rrc$x/data.ris.ripe.net/rrc$x/$month"
	cd ./rrc$x/data.ris.ripe.net/rrc$x/$month 
	python trackLinePrefix.py $prefix  > log_file$x
	cd -
	cp "./rrc$x/data.ris.ripe.net/rrc$x/$month/log_file$x" "./"
	cp "log_file$x" "./bases_beacon_rrc$collector/logs"
	rm "log_file$x"
done

for y in {log_file_bgpdata,log_file_linx,log_file_napafrica,log_file_saopaulo,log_file_sydney,log_file_wide}; do
	cp "../../route-views/beacon_logs_rv_$current_date/rrc$collector/$y" "./bases_beacon_rrc$collector/logs"
done



