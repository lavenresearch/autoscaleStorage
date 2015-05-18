#!/bin/sh

if [ "$#" = 0 ]; then
    echo "Run: ./deployStorage.sh iqn.2222."$(hostname)":storage.disk2 /home/suyiblock1G 2"
    deviceiqn=iqn.2222.$(hostname):storage.disk2
    setenforce 0
    dd if=/dev/zero of=/home/suyiblock1G bs=1M count=1000
    devicepath=/home/suyiblock1G
    tid=2
    gmip=192.168.3.137
elif [[ "$#" = 1 ]]; then
    echo "Run: ./deployStorage.sh iqn.2222."$(hostname)":storage.disk2 "${1}" 2"
    deviceiqn=iqn.2222.$(hostname):storage.disk2
    devicepath=${1}
    tid=2
    gmip=192.168.3.137
elif [[ "$#" = 2 ]]; then
    echo "Run: ./deployStorage.sh" ${1} ${2}" 2"
    deviceiqn=${1}
    devicepath=${2}
    tid=2
    gmip=192.168.3.137
elif [[ "$#" = 3 ]]; then
    echo "Run: ./deployStorage.sh" ${1} ${2} ${3}
    deviceiqn=${1}
    devicepath=${2}
    tid=${3}
    gmip=192.168.3.137
elif [[ "$#" = 4 ]]; then
    echo "Run: ./deployStorage.sh" ${1} ${2} ${3}
    deviceiqn=${1}
    devicepath=${2}
    tid=${3}
    gmip=${4}
else
    echo "Too much parameters!"
fi

# install iscsi target

yum install scsi-target-utils.x86_64 --nogpgcheck -y

# start iscsi target
status=$(service tgtd status)
if [[ $status = "tgtd is stopped" ]]; then
    /etc/init.d/tgtd start
fi

tgtadm --lld iscsi --op new --mode target --tid $tid -T $deviceiqn
setenforce 0 # have to gurantee SELinux off in order to use file instead block device.
tgtadm --lld iscsi --op new --mode logicalunit --tid $tid --lun 1 -b $devicepath
# tgtadm --lld iscsi --op bind --mode target --tid $tid -I ALL
tgtadm --lld iscsi --op bind --mode target --tid $tid -I $gmip