#!/bin/bash

updates="updates.20180701*"
 
mkdir bgpdata && cd bgpdata && pwd 
wget -A $updates -r -np -nc -l1 --no-check-certificate -e robots=off http://archive.routeviews.org/bgpdata/2018.07/UPDATES/ &
cd -
mkdir linx && cd linx && pwd 
wget -A $updates -r -np -nc -l1 --no-check-certificate -e robots=off http://archive.routeviews.org/route-views.linx/bgpdata/2018.07/UPDATES/ &
cd -
mkdir napafrica && cd napafrica && pwd 
wget -A $updates -r -np -nc -l1 --no-check-certificate -e robots=off http://archive.routeviews.org/route-views.napafrica/bgpdata/2018.07/UPDATES/ &
cd -
mkdir wide && cd wide && pwd 
wget -A $updates -r -np -nc -l1 --no-check-certificate -e robots=off http://archive.routeviews.org/route-views.wide/bgpdata/2018.07/UPDATES/ &
cd -
mkdir sydney && cd sydney && pwd 
wget -A $updates -r -np -nc -l1 --no-check-certificate -e robots=off http://archive.routeviews.org/route-views.sydney/bgpdata/2018.07/UPDATES/ &
cd -
mkdir saopaulo && cd saopaulo && pwd 
wget -A $updates -r -np -nc -l1 --no-check-certificate -e robots=off http://archive.routeviews.org/route-views.saopaulo/bgpdata/2018.07/UPDATES/ &
cd -

