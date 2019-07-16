#!/bin/bash

updates="updates.20181022*"

for x in {00,01,03,04,05,06,07,10,11,13,14,16}; do  
	mkdir rrc$x && cd rrc$x && pwd 
	wget -A $updates -r -np -nc -l1 --no-check-certificate -e robots=off http://data.ris.ripe.net/rrc$x/2018.10/ &
	cd ..
done
