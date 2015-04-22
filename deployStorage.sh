#!/bin/sh

if [ "$#" = 0 ]; then
    echo "Run: ./deployStorage.sh iqn.2222."$(hostname)":storage.disk2 /dev/sdb"
    deviceiqn=iqn.2222.$(hostname):storage.disk2
    devicepath=/dev/sdb
elif [[ "$#" = 1 ]]; then
    echo "Run: ./deployStorage.sh iqn.2222."$(hostname)":storage.disk2 "${1}
    deviceiqn=iqn.2222.$(hostname):storage.disk2
    devicepath=${1}
elif [[ "$#" = 2 ]]; then
    echo "Run: ./deployStorage.sh" ${1} ${2}
    deviceiqn=${1}
    devicepath=${2}
else
    echo "Too much parameters!"
fi

# install iscsi target

yum install scsi-target-utils.x86_64 -y

# start iscsi target

/etc/init.d/tgtd restart

tgtadm --lld iscsi --op new --mode target --tid 2 -T $deviceiqn
tgtadm --lld iscsi --op new --mode logicalunit --tid 2 --lun 1 -b $devicepath
tgtadm --lld iscsi --op bind --mode target --tid 2 -I ALL