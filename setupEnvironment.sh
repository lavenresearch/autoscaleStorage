#!/bin/sh

cluster=(192.168.1.162 192.168.1.131 192.168.1.137)
path=/usr/local/src/suyiAutoscale/

cd $path
cd ./src
dos2unix *
chmod +x *

for node in ${cluster[@]}
do
    # ssh-keygen -t rsa
    ssh-copy-id -i $node
    ssh -t root@$node "echo @;hostname"
    ssh -t root@$node "yum install iscsi-initiator-utils.x86_64 reiserfs-utils sysstat scsi-target-utils.x86_64 -y --nogpgcheck"
    ssh -t root@$node "service iptables stop"
    ssh -t root@$node "setenforce 0"
    ssh -t root@$node "lvmconf --disable-cluster"
    ssh -t root@$node "mkdir -p $path"
    scp -r $path/* $node:$path/
done