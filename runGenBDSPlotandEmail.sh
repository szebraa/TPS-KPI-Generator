#!/bin/bash
#use gzip -q (to zip) and gunzip -q (to unzip). -q will ignore all files that are already zipped or unzipped respectively
chmod 777 -R /home/sramanan/scripts/OneNDS/ndsstats
#gzip -q /home/sramanan/scripts/OneNDS/ndsstats/*
if [ "$1" == '-m' ];
then
    echo "please enter the start time in GMT (e.g.: 10:00:00): "
    read start_time
    echo "please enter the end time in GMT (e.g.: 18:00:00): "
    read end_time
    echo "Which email would you like the results send to? "
    read dest_email
    echo "Which date would you like to observe (note inputs must be entered as numbers... e.g.: 0 = today , 1 = yesterday, 2 = 2 days ago... etc)? "
    read req_date
    echo "please enter the interval you would like to use between data points (inputs are detected in seconds): "
    read interval
    echo "Do you want to produce the BDS TPS Graph? (y or n)? "
    read view_BDS_TPS
    echo "Do you want to produce the FDS TPS Graph? (y or n)? "
    read view_FDS_TPS
    /usr/bin/python /home/ubuntu/Scripts/genBDSPlotAndEmail.py $start_time $end_time $dest_email $req_date $interval $view_BDS_TPS $view_FDS_TPS
else
    /usr/bin/python /home/ubuntu/Scripts/genBDSPlotAndEmail.py "18:00:00" "22:30:00" "SDMSquad@bell.ca" 1 5 "y" "y"
fi
mv OneNDS_* /home/ubuntu/Scripts/
#touch /home/ubuntu/Scripts/test.txt
