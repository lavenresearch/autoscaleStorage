#!/bin/sh

if [ "$#" = 0 ]; then
    echo "Run: ./deployStorage.sh iqn.2222."$(hostname)":storage.disk2 /dev/sdb 2"
    deviceiqn=iqn.2222.$(hostname):storage.disk2
    devicepath=/dev/sdb
    tid=2
elif [[ "$#" = 1 ]]; then
    echo "Run: ./deployStorage.sh iqn.2222."$(hostname)":storage.disk2 "${1}" 2"
    deviceiqn=iqn.2222.$(hostname):storage.disk2
    devicepath=${1}
    tid=2

elif [[ "$#" = 2 ]]; then
    echo "Run: ./deployStorage.sh" ${1} ${2}" 2"
    deviceiqn=${1}
    devicepath=${2}
    tid=2
elif [[ "$#" = 3 ]]; then
    echo "Run: ./deployStorage.sh" ${1} ${2} ${3}
    deviceiqn=${1}
    devicepath=${2}
    tid=${3}
else
    echo "Too much parameters!"
fi

# install iscsi target

yum install scsi-target-utils.x86_64 -y

# start iscsi target
status=$(service tgtd status)
if [[ $status = "tgtd is stopped" ]]; then
    /etc/init.d/tgtd start
fi

tgtadm --lld iscsi --op new --mode target --tid $tid -T $deviceiqn
tgtadm --lld iscsi --op new --mode logicalunit --tid $tid --lun 1 -b $devicepath
tgtadm --lld iscsi --op bind --mode target --tid $tid -I ALL