#!/bin/sh

# setup iscsi initiator

yum install iscsi-initiator-utils.x86_64 -y

# 查看192.168.3.137上的目标
iscsiadm -m discovery -t sendtargets -p 192.168.3.121

deviceiqn=iqn.2222.test:storage.disk2

iscsiadm -m node -T $deviceiqn --login

# setup cluster lvm

yum install lvm2-cluster cman rgmanager -y

service iptables stop
setenforce 0
service NetworkManager stop
chkconfig NetworkManager off
# cp lvm.conf /etc/lvm/ -y
# cp cluser.conf /etc/cluster -y
lvmconf --enable-cluster
ccs_tool create testssdcluster1
ccs_tool addfence meatware fence_manual
ccs_tool addnode -n 1 -f meatware ca01
ccs_tool addnode -n 2 -f meatware ca02

# 修改hosts，127.0.0.1 不能对应主机名，主机ip需要对应主机名。

service cman start
service clvmd start

# 创建pv，vg，lv。此时在任何一台机器上的lvm操作都可以在另一台机器上提现出来。