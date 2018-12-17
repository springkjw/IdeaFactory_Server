#! /bin/bash
for each in `nmap -sP 192.168.0.0/24 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' `
do

    echo  $each
    nc -w 2 $each 22

    if [ $? -eq 0 ]
    then
        break;
    fi

done
ssh $each