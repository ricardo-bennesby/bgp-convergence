#!/bin/bash

#updates="updates.20110709*"
month="2018.07"
current_date="01_07_2018"

cd ..
mkdir beacon_logs_rv_$current_date && cd beacon_logs_rv_$current_date && pwd

for x in {00,01,03,04,05,06,07,10,11,13,14,16}; do
	mkdir rrc$x
	pwd
done

cd ../beacon_rv_$current_date



collector="00"
prefix="84.205.64.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="01"
prefix="84.205.65.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="03"
prefix="84.205.67.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="04"
prefix="84.205.68.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="05"
prefix="84.205.69.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="06"
prefix="84.205.70.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="07"
prefix="84.205.71.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="10"
prefix="84.205.74.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="11"
prefix="84.205.75.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="13"
prefix="84.205.77.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="14"
prefix="84.205.78.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done



collector="16"
prefix="84.205.73.0/24"

cp "./trackLinePrefix_route-views.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python trackLinePrefix_route-views.py $prefix > log_file_bgpdata
cd -
cp "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/log_file_bgpdata" "./"

for y in {linx,napafrica,saopaulo,sydney,wide}; do
	cp "./trackLinePrefix_route-views.py" "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/" 
	cd ./$y/archive.routeviews.org/route-views.$y/bgpdata/$month/UPDATES/
	python trackLinePrefix_route-views.py $prefix > log_file_$y
	cd -
	cp "./$y/archive.routeviews.org/route-views.$y/bgpdata/2018.07/UPDATES/log_file_$y" "./"	
done

for z in {bgpdata,linx,napafrica,saopaulo,sydney,wide}; do
	cp "./log_file_$z" "../beacon_logs_rv_$current_date/rrc$collector/"
	rm "log_file_$z"
done

