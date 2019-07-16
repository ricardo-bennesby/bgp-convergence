#!/bin/bash

month="2018.07"

cp "./list_files.py" "./linx/archive.routeviews.org/route-views.linx/bgpdata/2018.07/UPDATES/" 
cp "./mrt2bgpdump.py" "./linx/archive.routeviews.org/route-views.linx/bgpdata/2018.07/UPDATES/"
cd ./linx/archive.routeviews.org/route-views.linx/bgpdata/2018.07/UPDATES/
python list_files.py &
cd -

