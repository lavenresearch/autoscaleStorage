# de01 上启动target

status=$(service tgtd status)
if [[ $status = "tgtd is stopped" ]]; then
    /etc/init.d/tgtd start
fi
tgtadm --lld iscsi --op new --mode target --tid $tid -T $deviceiqn
tgtadm --lld iscsi --op new --mode logicalunit --tid $tid --lun 1 -b $devicepath
tgtadm --lld iscsi --op bind --mode target --tid $tid -I ALL

# ca01 上挂载

iscsiadm -m node -T iqn.2222.de01ca01:storage.disk2 -p 192.168.3.121 -l
mkreiserfs -f /dev/sde
mount -t reiserfs /dev/sde /autoscale

# 动态扩展

umount /autoscale
iscsiadm -m node -T iqn.2222.de01ca01:storage.disk2 -p 192.168.3.121 -u

# 在de01上执行
lvmextend -L 10G /dev/ssdmasterVG/ssdmasterLVca01
resize_reiserfs -f /dev/ssdmasterVG/ssdmasterLVca01
tgtadm --lld iscsi --op delete --mode target --tid $tid
tgtadm --lld iscsi --op new --mode target --tid $tid -T $deviceiqn
tgtadm --lld iscsi --op new --mode logicalunit --tid $tid --lun 1 -b $devicepath
tgtadm --lld iscsi --op bind --mode target --tid $tid -I ALL

# ca01 上挂载

iscsiadm -m node -T iqn.2222.de01ca01:storage.disk2 -p 192.168.3.121 -l
mount -t reiserfs /dev/sde /autoscale