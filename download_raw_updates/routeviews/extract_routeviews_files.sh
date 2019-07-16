#!/bin/bash

month="2018.07"

cp "./list_files.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/" 
cp "./mrt2bgpdump.py" "./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/"
cd ./bgpdata/archive.routeviews.org/bgpdata/2018.07/UPDATES/
python list_files.py &
cd -

cp "./list_files.py" "./napafrica/archive.routeviews.org/route-views.napafrica/bgpdata/2018.07/UPDATES/" 
cp "./mrt2bgpdump.py" "./napafrica/archive.routeviews.org/route-views.napafrica/bgpdata/2018.07/UPDATES/"
cd ./napafrica/archive.routeviews.org/route-views.napafrica/bgpdata/2018.07/UPDATES/
python list_files.py &
cd -

cp "./list_files.py" "./linx/archive.routeviews.org/route-views.linx/bgpdata/2018.07/UPDATES/" 
cp "./mrt2bgpdump.py" "./linx/archive.routeviews.org/route-views.linx/bgpdata/2018.07/UPDATES/"
cd ./linx/archive.routeviews.org/route-views.linx/bgpdata/2018.07/UPDATES/
python list_files.py &
cd -

cp "./list_files.py" "./saopaulo/archive.routeviews.org/route-views.saopaulo/bgpdata/2018.07/UPDATES/" 
cp "./mrt2bgpdump.py" "./saopaulo/archive.routeviews.org/route-views.saopaulo/bgpdata/2018.07/UPDATES/"
cd ./saopaulo/archive.routeviews.org/route-views.saopaulo/bgpdata/2018.07/UPDATES/
python list_files.py &
cd -

cp "./list_files.py" "./sydney/archive.routeviews.org/route-views.sydney/bgpdata/2018.07/UPDATES/" 
cp "./mrt2bgpdump.py" "./sydney/archive.routeviews.org/route-views.sydney/bgpdata/2018.07/UPDATES/"
cd ./sydney/archive.routeviews.org/route-views.sydney/bgpdata/2018.07/UPDATES/
python list_files.py &
cd -

cp "./list_files.py" "./wide/archive.routeviews.org/route-views.wide/bgpdata/2018.07/UPDATES/" 
cp "./mrt2bgpdump.py" "./wide/archive.routeviews.org/route-views.wide/bgpdata/2018.07/UPDATES/"
cd ./wide/archive.routeviews.org/route-views.wide/bgpdata/2018.07/UPDATES/
python list_files.py &
cd -
