tgtadm --lld iscsi --op new --mode target --tid 50 -T iqn.a.a:a.a
tgtadm --lld iscsi --op new --mode logicalunit --tid 50 --lun 1 -b /dev/loop0
tgtadm --lld iscsi --op bind --mode target --tid 50 -I ALL

iscsiadm -m discovery -t sendtargets -p 192.168.1.162
iscsiadm -m node -T iqn.a.a:a.a -p 192.168.1.162 -l



iscsiadm -m node -T iqn.a.a:a.a -p 192.168.1.162 -u

ssh -t root@192.168.1.162 "tgtadm --lld iscsi --op delete --mode target --tid 50"
ssh -t root@192.168.1.162 "lvchange -a n /dev/testvg/testlv && lvremove /dev/testvg/testlv"