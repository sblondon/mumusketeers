#! /bin/sh

PORT=8000
if [ `uname` = "Linux" ]
then
    IP_ADDRESS=`ip addr | grep -A 2 -E "(enp2s0|eth0)" | grep inet | grep -v inet6  | cut -d " " -f 6 | cut -d "/" -f 1`
else
    #IP_ADDRESS=`ifconfig | grep -A 2 "eth0" | grep 'inet adr:' | cut -d " " -f 12  | cut -d ":" -f 2`
    IP_ADDRESS=`ifconfig | grep -A 5 "en0" | grep 'inet ' | cut -d " " -f 2`
fi

echo "\tLe service est sur http://${IP_ADDRESS}:${PORT}"

